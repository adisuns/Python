"""
ask the user to enter a word;
use userWord = userWord.upper() to convert the word entered by the user to upper case; we'll talk about the so-called string methods and the upper() method very soon - don't worry;
use conditional execution and the continue statement to "eat" the following vowels A, E, I, O, U from the inputted word;
print the uneaten letters to the screen, each one of them on a separate line.
"""
vovel = ["A","E","I","O","U"]
input_string = input("Enter any word")
input_string = input_string.upper()
for c in input_string:
    if c in vovel:
        input_string = input_string.replace(c,"")
        continue
for character in input_string:
    print(character)