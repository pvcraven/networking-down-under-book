# Enable ANSI graphics for Windows DOS prompt
import colorama
colorama.init()

# --- Print a table of ANSI characters
print("Decimal Hex    Character")
for i in range(106, 121):
    char = chr(i)
    print("{:3}     0x{:0x}   \x1b(0{}\x1b(B          ".format(i, i, char))
    print()

print()

# --- Print a sine wave

# Lines down
for i in range(111, 116):
    char = chr(i)
    print("\x1b(0{}\x1b(B".format(char), end="")

# Lines up
for i in range(115, 110, -1):
    char = chr(i)
    print("\x1b(0{}\x1b(B".format(char), end="")

# Lines down
for i in range(111, 116):
    char = chr(i)
    print("\x1b(0{}\x1b(B".format(char), end="")

    
print()
print()

# --- Print a box with text in it

# Top-right corner
char = chr(108)
print("\x1b(0{}\x1b(B".format(char), end="")

# Horizontal line
for i in range(10):
    char = chr(113)
    print("\x1b(0{}\x1b(B".format(char), end="")

# Top-left corner
char = chr(107)
print("\x1b(0{}\x1b(B".format(char), end="")

print()

# Vertical line
char = chr(120)
print("\x1b(0{}\x1b(B".format(char), end="")

# Text in the box
print(" ANSI Box ", end="")

# Vertical line
char = chr(120)
print("\x1b(0{}\x1b(B".format(char), end="")

print()

# Bottom-left corner
char = chr(109)
print("\x1b(0{}\x1b(B".format(char), end="")

# Horizontal line
for i in range(10):
    char = chr(113)
    print("\x1b(0{}\x1b(B".format(char), end="")

# Bottom-right corner
char = chr(106)
print("\x1b(0{}\x1b(B".format(char), end="")


print()
