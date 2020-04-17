"""
calculate height of pyramid using number of blocks
"""
number_of_blocks = int(input("Enter number of blocks "))
height = 0
rows = 0
used_blocks = 0
while used_blocks < number_of_blocks:
        rows += 1 #new row
        used_blocks += rows # adding same number of blocks as that of rows
        height +=1
print("pyramid with total ",number_of_blocks," will be of height",height)



