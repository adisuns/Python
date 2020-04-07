"""
Your task is very simple here: write a program that uses a for loop to "count mississippily" to five. Having counted to five,
the program should print to the screen the final message "Ready or not, here I come!"
"""
import time
counter = 5
for i in range(1,counter+1):
    time.sleep(1.0)
    print(i,"mississippily")
print("Ready or not here i come")
