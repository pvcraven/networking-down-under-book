# Enable ANSI graphics for Windows DOS prompt
import colorama
colorama.init()

# Define colors
# \x says there is a hex number coming.
# 1B in hex is an "escape" character.
# [ starts the sequence, and m ends it.
# 31 is for red. 32 green.
# 0 will reset everything.
# 1 will bold the text.
BRIGHT_RED = "\x1b[1;31m"
RED = "\x1b[31m"
GREEN = "\x1b[32m"
RESET = "\x1b[0m"

# Clear the screen
CLEAR_SCREEN = "\x1b[2J"

# Special ANSI characters you can draw boxes with
BOTTOM_RIGHT_BOX = "\x1b(0\x6a\x1bB("
TOP_RIGHT_BOX = "\x1b(0\x6b\x1bB("
TOP_LEFT_BOX = "\x1b(0\x6c\x1bB("
BOTTOM_LEFT_BOX = "\x1b(0\x6d\x1bB("
CROSS = "\x1b(0\x6e\x1bB("
HORIZONTAL = "\x1b(0\x71\x1bB("
VERTICAL = "\x1b(0\x78\x1bB("

# Print some colored text
print(CLEAR_SCREEN, end="")
print(f"Adding colors is {BRIGHT_RED}great{RESET} to do.")
print(f"This {GREEN}is in green{RESET}.")

# Print a table of ANSI characters.
# If you are running on Windows, these might not look right.
# You may need to run it in Windows Terminal or some other
# terminal program with full ANSI support.
for i in range(0x21, 0x7e):
	if i % 8 == 0:
		print()
	char = chr(i)
	hex_string = f"0x{i:0x}"
	ansi_character = f"\x1b(0{char}\x1b(B"
	print(f"{hex_string} {ansi_character}", end="  ")

print()
