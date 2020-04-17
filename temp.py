blocks = int(input("Enter number of blocks: "))
height = 0
by_row = 0
total = 0
for i in range(blocks):
    if blocks <= total:
        break
    height += 1
    by_row += 1
    total += by_row

print(f"The height of the pyramid:{height}")