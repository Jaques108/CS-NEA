listA = [3,9,16,7,102,1,6]
oddNums = []
highestNum = listA[0]
total = 0
length = len(listA)

afile = open('oddNums.txt','a')

for i in range(length):
    temp = listA[i]

    if highestNum < temp:
        highestNum = temp

    if temp % 2 != 0:
        oddNums.append(temp)
        afile.write(str(temp) + ",")



    total += temp
    average = round(total/length,4)


numbers = 0

while numbers < 3:
    num = int(input('Enter an odd number: '))

    if num % 2 != 0:
        afile.write(str(num) + ",")
        numbers += 1



afile = open('oddNums.txt','r')


print(highestNum,total,average,oddNums)
print(afile.read())