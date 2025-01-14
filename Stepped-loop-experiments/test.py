state = [1, [2, 3, [4, 5]], 6]

index_list = [1, 2, 0]

depth = len(index_list)

parent_item = None
current_item = state[index_list[0]]

for i in range(1, depth):

    parent_item = current_item
    current_item = parent_item[index_list[i]]

print(parent_item)
print(current_item)