def is_increasing_safe(entries: list):
    last = entries[0]
    for entry in entries[1:]:
        score = entry - last
        if score >3 or score <1:
            return False
        else:
            last = entry
    return True

def is_safe(entries, whithout: int = None):
    if whithout is not None:
        entries = entries[:whithout] + entries[whithout + 1:]
    reversed_entries = entries[::-1]
    return is_increasing_safe(entries) or is_increasing_safe(reversed_entries)

s1 = 0
s2 = 0
with open("input.txt", "r") as file:
    for line in file:
        entries = [int(raw_entry) for raw_entry in line.strip().split(" ")]
        if is_safe(entries):
            s1 += 1
            s2 += 1
        elif any([is_safe(entries, i) for i in range(len(entries))]):
            s2 +=1

print("Part1 is:", s1)
print("Part 2 is:", s2)