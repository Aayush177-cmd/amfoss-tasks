import os
import time
import curses


previous_cpu = {}
previous_time = time.time()


def get_memory_usage(pid):
    try:
        with open(f"/proc/{pid}/status", "r") as file:
            for line in file:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1]) / 1024

    except (FileNotFoundError, PermissionError):
        pass

    return 0.0


def get_process_cpu_time(pid):
    try:
        with open(f"/proc/{pid}/stat", "r") as file:
            values = file.read().split()

        utime = int(values[13])
        stime = int(values[14])

        return utime + stime

    except (FileNotFoundError, PermissionError, ValueError):
        return 0


def get_processes():

    global previous_time

    current_time = time.time()
    processes = []

    clock_ticks = os.sysconf(
        os.sysconf_names["SC_CLK_TCK"]
    )

    for entry in os.listdir("/proc"):

        if not entry.isdigit():
            continue

        pid = entry

        try:

            with open(f"/proc/{pid}/comm", "r") as file:
                name = file.read().strip()

            current_cpu = get_process_cpu_time(pid)

            if pid in previous_cpu:

                cpu_difference = current_cpu - previous_cpu[pid]
                time_difference = current_time - previous_time

                cpu_seconds = cpu_difference / clock_ticks

                if time_difference > 0:
                    cpu_percentage = (
                        cpu_seconds / time_difference
                    ) * 100
                else:
                    cpu_percentage = 0

            else:
                cpu_percentage = 0

            previous_cpu[pid] = current_cpu

            memory = get_memory_usage(pid)

            processes.append({
                "pid": pid,
                "name": name,
                "cpu": cpu_percentage,
                "memory": memory
            })

        except (FileNotFoundError, PermissionError):
            continue

    previous_time = current_time

    processes.sort(
        key=lambda process: process["cpu"],
        reverse=True
    )

    return processes


def draw_screen(stdscr, processes, selected):

    stdscr.erase()

    height, width = stdscr.getmaxyx()

    title = "🏴‍☠️ GRAND LINE GUARDIAN"

    stdscr.addstr(
        0,
        0,
        title[:width - 1],
        curses.A_BOLD
    )

    stdscr.addstr(
        1,
        0,
        f"Total Active Processes: {len(processes)}"
    )

    stdscr.addstr(
        3,
        0,
        f"{'PID':<10}{'PROCESS NAME':<30}"
        f"{'CPU %':<10}{'MEMORY (MB)':<12}"
    )

    stdscr.addstr(
        4,
        0,
        "-" * min(width - 1, 65)
    )

    max_rows = height - 7

    for index, process in enumerate(processes[:max_rows]):

        line = (
            f"{process['pid']:<10}"
            f"{process['name']:<30}"
            f"{process['cpu']:<10.2f}"
            f"{process['memory']:<12.2f}"
        )

        if index == selected:

            stdscr.addstr(
                index + 4,
                0,
                line[:width - 1],
                curses.A_REVERSE
            )

        else:

            stdscr.addstr(
                index + 4,
                0,
                line[:width - 1]
            )

    footer_y = height - 2

    stdscr.addstr(
        footer_y,
        0,
        "↑/↓ Navigate    k Kill    q Quit"
        [:width - 1],
        curses.A_BOLD
    )

    stdscr.refresh()


def main(stdscr):

    global previous_time

    curses.curs_set(0)

    stdscr.nodelay(True)

    selected = 0

    while True:

        processes = get_processes()

        if processes:

            if selected >= len(processes):
                selected = len(processes) - 1

        else:
            selected = 0

        draw_screen(
            stdscr,
            processes,
            selected
        )

        key = stdscr.getch()

        if key == ord("q"):
            break

        elif key == ord("k"):

            if processes:

                pid = processes[selected]["pid"]

                stdscr.nodelay(False)

                stdscr.addstr(
                1,
                0,
                f"Terminate PID {pid}? Press y/n: "
                )

                stdscr.refresh()

                answer = stdscr.getch()

                if answer == ord("y"):

                    kill_process(pid)

                stdscr.nodelay(True)


        elif key == curses.KEY_UP:

            if selected > 0:
                selected -= 1

        elif key == curses.KEY_DOWN:

            if selected < len(processes) - 1:
                selected += 1

        time.sleep(0.5)

def kill_process(pid):
    try:
        os.kill(int(pid), 15)  # SIGTERM
        return True

    except (ProcessLookupError, PermissionError, ValueError):
        return False


curses.wrapper(main)