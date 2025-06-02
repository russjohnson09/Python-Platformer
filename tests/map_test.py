
import os

# current_dir = os.path.realpath(__file__)
current_dir = os.path.dirname(__file__)

file_path = os.path.join(current_dir, "test.txt")

with open(file_path) as f:
    row = 0
    col = 0
    for line in f:
        col = 0
        for char in line:
            # print(char)
            print(row,col)
            col += 1
        row += 1
        #print(line)

       # For Python3, use print(line)
       #if 'str' in line:
        #  break


print("end")