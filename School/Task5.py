import os

sentence = input('Enter a sentence: ')


if sentence[0].islower():
    sentence = sentence[0].upper() + sentence[1:]
    print(sentence)

firstWord = ''

for i in range(len(sentence)):
    temp = sentence[i]

    if temp == ' ':
        break

    else:
        firstWord += temp


if os.path.exists('Words.txt'):
    afile = open('Words.txt','a')
    afile.write(firstWord + sentence[-4:])
    afile.close()

else:
    afile = open('Words.txt', 'w')
    afile.write(firstWord + sentence[-4:])
    afile.close()


afile = open('Words.txt','r')
contents = afile.read()
afile.close()

print(contents)

