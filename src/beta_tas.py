from pynput.keyboard import Controller, Key
from time import sleep, perf_counter
from sys import platform
import re

get_scanner = [
    "scanner_1.txt",
    # "soft_reset.txt",
    "scanner_2.txt",
]

nested_files = [
    "full_reset.txt",
    get_scanner,
]

files = []
for file in nested_files:
    if isinstance(file, list):
        files.extend(file)
    else:
        files.append(file)
# --- Load moves ---
moves = []
for file in files:
    if platform == "win32":
        current_path = "assets\\" + file
    else:
        current_path = "assets/" + file

    with open(current_path, "r") as f:
        current_moves = [line.strip() for line in f if line.strip()]
    
    moves.extend(current_moves)

# --- Key Mapping ---
def char_to_key(char):
    mapping = {
        "u": Key.up,
        "d": Key.down,
        "l": Key.left,
        "r": Key.right,

        "e": Key.esc,
        "s": Key.space
    }
    return mapping.get(char, char)  # if not mapped, treat as normal character

# --- Parse line like zl10 into ([Key.z, Key.left], 10) ---
def parse_line(line):
    match = re.match(r"([a-zA-Z]+)(\d*)", line)
    if not match:
        raise ValueError(f"Invalid line format: {line}")

    key_part, frame_part = match.groups()
    keys = [char_to_key(c) for c in key_part]
    frames = int(frame_part) if frame_part else 1  # default to 1 frame if omitted

    return keys, frames

# --- Run Keys with precise timing ---
def runKeys(moves):
    kb = Controller()
    frame_time = 1 / 20  # 0.05 seconds per frame

    for line in moves:
        keys, frames = parse_line(line)
        print(f"Pressing {keys} for {frames} frames")

        for _ in range(frames):
            start_time = perf_counter()

            # Press keys
            for key in keys:
                kb.press(key)

            # Wait until next frame cycle
            middle_time = perf_counter();
            elapsed_time = middle_time - start_time
            sleep_time = max(0, frame_time - 2*elapsed_time) # it will take roughly the same amount of time to press the keys as to release it, so we account for both
            sleep(sleep_time)

            # Release keys
            for key in keys:
                kb.release(key)
            end_time = perf_counter()
            elapsed_time = end_time - start_time
            sleep_time = max(0, frame_time - elapsed_time) # wait any remaining time until the full length is reached

# --- Run ---
sleep(0.50)
print("START")
runKeys(moves)
print("FINISHED")