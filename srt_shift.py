from datetime import datetime, timedelta


class Entry:
    def __init__(self, start, end, lines):
        self.start, self.end, self.lines = start, end, lines


def get_srt_file_content(path):
    with open(path, "r") as f:
        text = f.read()

    lines = text.split("\n")

    entries = []
    i = 0
    fmt = "%H:%M:%S,%f"
    while 1:
        i += 1
        if i >= len(lines):
            break
        time_line = lines[i]
        i += 1
        content_lines = []
        line = lines[i]
        while line:
            content_lines.append(line)
            i += 1
            line = lines[i]
        time_strings = time_line.split(" --> ")
        start = datetime.strptime(time_strings[0], fmt)
        end = datetime.strptime(time_strings[1], fmt)
        entries.append(Entry(start, end, content_lines))
        i += 1

    return entries


def shift_entries(entries, delta):
    delta_ms = int(delta)
    for entry in entries:
        entry.start += timedelta(milliseconds=delta_ms)
        entry.end += timedelta(milliseconds=delta_ms)


def write_entries(entries, path):
    fmt = "{0:%H:%M:%S,%f}"
    with open(path, "w") as f:
        for i, entry in enumerate(entries):
            f.write(str(i) + "\n")
            start_str = fmt.format(entry.start)[:-3]
            end_str = fmt.format(entry.end)[:-3]
            f.write("{} --> {}\n".format(start_str, end_str))
            for line in entry.lines:
                f.write(line + "\n")
            f.write("\n")


def shift_srt(path, delta):
    entries = get_srt_file_content(path)
    shift_entries(entries, delta)
    write_entries(entries, path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Shift an srt file by tot seconds")
    parser.add_argument("-f", "--file", required=True,
                        help="The path to the srt file to be shifted, the script modifies the file in-place.")
    parser.add_argument("-d", "--delta", required=True,
                        help="The time delta to apply in milliseconds (integer please).")
    args = parser.parse_args()
    file = args.file
    delta = args.delta
    shift_srt(file, delta)
