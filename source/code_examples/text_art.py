"""
Text Art
"""
size = int(input("Enter size of design (1-9): "))

# Loop for each row, 1 to SIZE (inclusive)
for i in range(1, size + 1):
    # Print leading spaces
    for j in range(size - i):
        print(" ", end=" ")
    # Count up
    for j in range(1, i + 1):
        print(j, end=" ")
    # Count down
    for j in range(i - 1, 0, -1):
        print(j, end=" ")
    # Advance to the next row
    print()

# Loop each row, 1 to SIZE - 1.
# (Don't repeat the middle row)
for i in range(1, size):
    # Print leading spaces
    for j in range(i):
        print(" ", end=" ")
    # Count up
    for j in range(1, size - i):
        print(j, end=" ")
    # Count down
    for j in range(size - i, 0, -1):
        print(j, end=" ")
    # Advance to the next row
    print()