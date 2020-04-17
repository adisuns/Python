#Create a program with a for loop and a break statement. The program should iterate over characters in an email address, exit the loop when it reaches the @ symbol,
# and print the part before @ on one line. Use the skeleton below:
user_email = "someemail@mail.com"
for character in user_email:
    if character == '@':
        break
    print(character,end="")
