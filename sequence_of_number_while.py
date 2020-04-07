# A program that reads a sequence of numbers
# and counts how many numbers are even and how many are odd.
# The program terminates when zero is entered.
odd_numbers = 0
even_numbers = 0
new_number = int(input("Enter any number "))
while new_number !=0:
    if new_number % 2 == 1:
        odd_numbers += 1
    else:
        even_numbers += 1
    new_number = int(input("Enter any integer and 0 to exit"))
print("Odd numbers count:", odd_numbers)
print("Even numbers count:", even_numbers)