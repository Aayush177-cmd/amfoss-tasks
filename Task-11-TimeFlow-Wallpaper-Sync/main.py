from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os
import time
import threading


TEXT_FILE = "notes.txt"
WALLPAPER_FILE = "wallpaper.png"

WIDTH = 1920
HEIGHT = 1080

content_lock = threading.Lock()
file_content = ""
file_changed = True


class FileChangeHandler(FileSystemEventHandler):

    def update_file(self):
        global file_changed

        with content_lock:
            file_changed = True

        print("\nText file changed. Updating content...")

    def on_modified(self, event):
        if os.path.abspath(event.src_path) == os.path.abspath(TEXT_FILE):
            self.update_file()

    def on_created(self, event):
        if os.path.abspath(event.src_path) == os.path.abspath(TEXT_FILE):
            self.update_file()

    def on_deleted(self, event):
        if os.path.abspath(event.src_path) == os.path.abspath(TEXT_FILE):
            self.update_file()


def read_text_file():

    if not os.path.exists(TEXT_FILE):
        return "File not found: notes.txt"

    try:
        with open(TEXT_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()

    except Exception as error:
        return f"Unable to read file: {error}"

    if not content:
        return "The file is empty."

    return content


def get_font(size, bold=False):

    if bold:
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
        ]
    else:
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"
        ]

    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


def create_gradient(width, height):

    image = Image.new("RGB", (width, height))
    pixels = image.load()

    top_color = (18, 12, 45)
    middle_color = (42, 25, 85)
    bottom_color = (10, 35, 70)

    for y in range(height):

        position = y / height

        if position < 0.5:

            ratio = position * 2

            r = int(top_color[0] * (1 - ratio) + middle_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + middle_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + middle_color[2] * ratio)

        else:

            ratio = (position - 0.5) * 2

            r = int(middle_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(middle_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(middle_color[2] * (1 - ratio) + bottom_color[2] * ratio)

        for x in range(width):
            pixels[x, y] = (r, g, b)

    return image


def wrap_text(draw, text, font, max_width):

    lines = []

    for paragraph in text.splitlines():

        words = paragraph.split()

        if not words:
            lines.append("")
            continue

        current_line = words[0]

        for word in words[1:]:

            test_line = current_line + " " + word

            bbox = draw.textbbox(
                (0, 0),
                test_line,
                font=font
            )

            text_width = bbox[2] - bbox[0]

            if text_width <= max_width:
                current_line = test_line

            else:
                lines.append(current_line)
                current_line = word

        lines.append(current_line)

    return lines


def create_wallpaper(content):

    image = create_gradient(WIDTH, HEIGHT)

    draw = ImageDraw.Draw(image)

    # Fonts

    title_font = get_font(70, True)
    subtitle_font = get_font(28)
    clock_font = get_font(92, True)
    date_font = get_font(28)
    heading_font = get_font(34, True)
    text_font = get_font(28)
    footer_font = get_font(24)

    # Colors

    WHITE = (245, 245, 255)
    LIGHT_TEXT = (210, 210, 230)
    MUTED = (160, 160, 190)

    CYAN = (80, 200, 255)
    PURPLE = (100, 120, 255)
    PINK = (80, 150, 255)

    PANEL = (20, 30, 60)
    CLOCK_PANEL = (30, 45, 90)

    # Decorative circles

    draw.ellipse(
        (WIDTH - 500, -250, WIDTH + 150, 400),
        fill=(70, 40, 130)
    )

    draw.ellipse(
        (-250, HEIGHT - 350, 350, HEIGHT + 250),
        fill=(20, 80, 130)
    )

    # App title

    draw.text(
        (100, 70),
        "TIMEFLOW",
        font=title_font,
        fill=WHITE
    )

    draw.text(
        (105, 155),
        "Your notes. Your time. Your desktop.",
        font=subtitle_font,
        fill=CYAN
    )

    # Clock card

    clock_x1 = 1300
    clock_y1 = 60
    clock_x2 = 1820
    clock_y2 = 250

    draw.rounded_rectangle(
        (clock_x1, clock_y1, clock_x2, clock_y2),
        radius=35,
        fill=CLOCK_PANEL,
        outline=PURPLE,
        width=3
    )

    current_time = datetime.now().strftime("%H:%M:%S")

    time_bbox = draw.textbbox(
        (0, 0),
        current_time,
        font=clock_font
    )

    time_width = time_bbox[2] - time_bbox[0]

    draw.text(
        (
            clock_x1 + (clock_x2 - clock_x1 - time_width) // 2,
            80
        ),
        current_time,
        font=clock_font,
        fill=WHITE
    )

    current_date = datetime.now().strftime(
        "%A, %d %B %Y"
    )

    date_bbox = draw.textbbox(
        (0, 0),
        current_date,
        font=date_font
    )

    date_width = date_bbox[2] - date_bbox[0]

    draw.text(
        (
            clock_x1 + (clock_x2 - clock_x1 - date_width) // 2,
            190
        ),
        current_date,
        font=date_font,
        fill=CYAN
    )

    # Notes panel

    panel_x1 = 100
    panel_y1 = 270
    panel_x2 = 1820
    panel_y2 = 930

    draw.rounded_rectangle(
        (panel_x1, panel_y1, panel_x2, panel_y2),
        radius=40,
        fill=PANEL,
        outline=(70, 70, 130),
        width=2
    )

    # Accent line

    draw.rounded_rectangle(
        (100, 270, 115, 930),
        radius=8,
        fill=PINK
    )

    # Notes heading

    draw.text(
        (155, 315),
        "MY NOTES",
        font=heading_font,
        fill=WHITE
    )

    # LIVE indicator

    draw.ellipse(
        (1650, 325, 1670, 345),
        fill=CYAN
    )

    draw.text(
        (1685, 315),
        "LIVE",
        font=subtitle_font,
        fill=CYAN
    )

    # Divider

    draw.line(
        (155, 385, 1765, 385),
        fill=(75, 75, 120),
        width=2
    )

    # Wrap content

    lines = wrap_text(
        draw,
        content,
        text_font,
        1550
    )

    y = 430
    line_spacing = 42

    for line in lines:

        if y + line_spacing > 920:

            draw.text(
                (155, y),
                "...",
                font=text_font,
                fill=MUTED
            )

            break

        draw.text(
            (155, y),
            line,
            font=text_font,
            fill=LIGHT_TEXT
        )

        y += line_spacing

    # Footer

    footer_y = 980

    draw.ellipse(
        (100, footer_y + 7, 115, footer_y + 22),
        fill=CYAN
    )

    draw.text(
        (130, footer_y),
        "Monitoring notes.txt",
        font=footer_font,
        fill=LIGHT_TEXT
    )

    last_sync = datetime.now().strftime("%H:%M:%S")

    sync_text = f"Last sync: {last_sync}"

    sync_bbox = draw.textbbox(
        (0, 0),
        sync_text,
        font=footer_font
    )

    sync_width = sync_bbox[2] - sync_bbox[0]

    draw.text(
        (WIDTH - sync_width - 100, footer_y),
        sync_text,
        font=footer_font,
        fill=MUTED
    )

    image.save(WALLPAPER_FILE)

    return current_time


def set_wallpaper():

    wallpaper_path = os.path.abspath(WALLPAPER_FILE)

    subprocess.run(
        [
            "gsettings",
            "set",
            "org.gnome.desktop.background",
            "picture-uri",
            f"file://{wallpaper_path}"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    subprocess.run(
        [
            "gsettings",
            "set",
            "org.gnome.desktop.background",
            "picture-uri-dark",
            f"file://{wallpaper_path}"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def load_file_content():

    global file_content

    with content_lock:
        file_content = read_text_file()


def monitor_file():

    folder = os.path.abspath(".")

    event_handler = FileChangeHandler()

    observer = Observer()

    observer.schedule(
        event_handler,
        folder,
        recursive=False
    )

    observer.start()

    return observer


def main():

    global file_content
    global file_changed

    print("TimeFlow Wallpaper Sync")
    print("------------------------")
    print("Monitoring:", os.path.abspath(TEXT_FILE))
    print("Press Ctrl+C to stop.")

    load_file_content()

    observer = monitor_file()

    try:

        while True:

            with content_lock:

                if file_changed:

                    file_content = read_text_file()
                    file_changed = False

                current_content = file_content

            current_time = create_wallpaper(
                current_content
            )

            set_wallpaper()

            print(
                f"Current time: {current_time}",
                end="\r"
            )

            time.sleep(1)

    except KeyboardInterrupt:

        print("\nStopping TimeFlow...")

        observer.stop()
        observer.join()

        print("TimeFlow stopped.")


if __name__ == "__main__":
    main()