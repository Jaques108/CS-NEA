
items = ['Train','Car','Horse','Taxi','Foot','Bike']

items.sort()

items.append('Scooter')

item = 'Horse'
if item in items:
    items.remove(item)


item = 'Rabbit'
if item in items:
    items.remove(item)


items.insert(2,'Donkey')

index = items.index('Taxi')

items.insert(index,'Aeroplane')

items.append('Car')

seen = set()
for item in items:
    if item in seen:
        items.remove(item)
    else:
        seen.add(item)

