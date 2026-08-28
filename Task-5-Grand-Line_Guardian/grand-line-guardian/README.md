# Grand Line Guardian

Grand Line Guardian is a terminal-based system monitoring tool for Linux. It is inspired by tools like 'htop' and displays information about currently running processes.

The program reads process information directly from the Linux '/proc' virtual filesystem and updates the display in real time.

## Features

- Displays Process ID (PID)
- Displays process name
- Displays CPU usage
- Displays memory usage in MB
- Displays the total number of active processes
- Refreshes automatically every 0.5 seconds
- Sorts processes based on CPU usage
- Navigate through processes using the arrow keys
- Terminate a selected process
- Confirmation before terminating a process
- Quit the application using 'q'

## Requirements

- Linux operating system
- Python 3
- Terminal with `curses` support

The project uses only Python standard libraries, so no external packages are required.

## How it works

Linux provides information about running processes through the '/proc' virtual filesystem.

Each running process has a directory inside '/proc' named after its Process ID.

For example:

/proc/1
/proc/100
/proc/1234

The program scans /proc and reads information from the following files.

### Process name

The process name is read from:

/proc/<PID>/comm

### Memory usage

Memory information is read from:

/proc/<PID>/status


The program uses the 'VmRSS' value to find the physical memory currently being used by the process.

### CPU usage

CPU information is read from:

/proc/<PID>/stat

The program reads the CPU time used by a process and compares it with the previous reading to calculate CPU usage over a time interval.

## Project Structure

grand-line-guardian/
 main.py
 requirements.txt

## Running the project

Clone the repository:

git clone <repository-url>

Go into the project directory:

cd grand-line-guardian

Run the program:

python3 main.py


## Keyboard Controls

| Key | Action |
| Up Arrow | Move selection up |
| Down Arrow | Move selection down |
| 'k' | Terminate selected process |
| 'q' | Quit the program |

When 'k' is pressed, the program asks for confirmation before terminating the selected process.

## Testing process termination

To safely test the termination feature, open another terminal and run:

sleep 1000

Then find the 'sleep' process in Grand Line Guardian, select it, and press 'k'.

Avoid terminating system processes or processes that you do not recognize.

## Concepts learned

While working on this project, I learned about:

- Linux process management
- Process IDs
- The '/proc' virtual filesystem
- Reading process information from the Linux kernel
- CPU usage calculation
- Memory usage using 'VmRSS'
- Process signals and termination
- Real-time monitoring
- Building terminal interfaces using Python 'curses'

## Resources used

- Linux '/proc' filesystem documentation
- Python documentation for 'os'
- Python documentation for 'time'
- Python documentation for 'curses'

## Future improvements

Some possible improvements include:

- Sorting processes by memory usage
- Searching for processes
- Filtering processes
- Displaying system-wide CPU usage
- Displaying total system memory
- Adding colors to the interface
- Showing more details about a selected process

## Conclusion

Grand Line Guardian is a simple system monitoring tool that reads information about running Linux processes using the '/proc' filesystem.

It provides a real-time view of processes along with their PID, name, CPU usage, memory usage, and the total number of active processes. It also includes keyboard navigation and the ability to terminate a selected process.
