s1 = 0
s2 = 0

directions = [(i,j) for i in [-1,0,1] for j in [-1,0,1] if i != 0 or j !=0]
with open("input.txt", "r") as file:
    data = [line.strip() for line in file]
    height = len(data)
    width = len(data[0])
    for i in range(width):
        for j in range(height):
            if data[i][j] == 'X':
                for direction in directions:
                    valid = True
                    for ((current_i, current_j), expected) in zip(((i+direction[0]*d,j+direction[1]*d) for d in range(1,5)), ("M","A","S")):
                        if current_i not in range(width) or current_j not in range(height) or data[current_i][current_j] != expected:
                            valid = False
                            break
                    if valid:
                        s1 +=1
            if i in range(1,width-1) and j in range(1, height-1):
                if data[i][j] == 'A':
                    if {data[i-1][j-1], data[i+1][j+1]} == {"M","S"} and {data[i-1][j+1], data[i+1][j-1]} == {"M","S"}:
                        s2 +=1

print("Part1 is:", s1)
print("Part 2 is:", s2)