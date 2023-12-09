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
    # Advance to the next row
    print()

