"""
Design a program that uses a while loop and continuously asks the user to enter a word unless the user enters "chupacabra" as the secret exit word,
in which case the message "You've successfully left the loop." should be printed to the screen, and the loop should terminate.
"""
secrete_word = "chupacabra"
input_word = ""
while input_word != secrete_word:
    input_word = input("Enter any word ")
    if input_word == secrete_word:
        print("you have successfully left the loop")
        break
