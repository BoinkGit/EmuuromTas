from pynput.keyboard import Controller, Key
from time import sleep
from sys import platform
import re

# --- Load move list ---
if platform == "win32":
    moves_path = "assets\\get_scanner.txt"
else:
    moves_path = "assets/get_scanner.txt"

with open(moves_path, "r") as f:
    moves = [line.strip() for line in f if line.strip()]

# --- Key Mapping ---
def char_to_key(char):
    mapping = {
        "u": Key.up,
        "d": Key.down,
        "l": Key.left,
        "r": Key.right,
        "e": Key.esc
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

# --- Send Keys ---
def runKeys(moves):
    kb = Controller()
    for line in moves:
        keys, frames = parse_line(line)
        print(f"Pressing {keys} for {frames} frames")
        for i in range(frames):
            for key in keys:
                kb.press(key)
            sleep(0.05)
            for key in keys:
                kb.release(key)

# --- Run ---
sleep(0.50)
print("START")
runKeys(moves)
print("FINISHED")