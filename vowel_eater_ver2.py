"""
ask the user to enter a word;
use userWord = userWord.upper() to convert the word entered by the user to upper case; we'll talk about the so-called string methods and the upper() method very soon - don't worry;
use conditional execution and the continue statement to "eat" the following vowels A, E, I, O, U from the inputted word;
print the uneaten letters to the screen, each one of them on a separate line.
"""
wordWithoutVovels = ""
userWord = input("Enter any word ")
userWord = userWord.upper()

for letter in userWord:
    if letter == 'A':
        continue
    elif letter == 'E':
        continue
    elif letter == 'I':
        continue
    elif letter == 'O':
        continue
    elif letter == 'U':
        continue
    else:
        wordWithoutVovels += letter
        continue
print(wordWithoutVovels)