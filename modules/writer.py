#This module contains a function named writenow that writes the input into a book.txt file

def writenow(words):
    txt = open('book.txt', 'w+')
    txt.write(words)
    txt.close()