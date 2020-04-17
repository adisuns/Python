input_number = int(input("Enter any positive non zero number"))
steps = 0
while input_number != 1:
    if input_number % 2 ==0: #number is even
        input_number = input_number / 2
        print(int(input_number))
        steps += 1
    else: #number is odd
        input_number = 3 * input_number + 1
        print(int(input_number))
        steps += 1
print("total steps ",steps)