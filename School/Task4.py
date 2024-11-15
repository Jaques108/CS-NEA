array = [1,2,3,3,4,5,6,6,7,7,8,9]


def removeDuplicates(array):
    seen = set()
    for item in array:
        if item in seen:
            array.remove(item)
        else:
            seen.add(item)

    return array




print(removeDuplicates(array))