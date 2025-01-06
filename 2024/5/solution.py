from collections import defaultdict
from typing import List
import sys

rules = defaultdict(list)
updates = []

def score(update: List[int]):
    for i, step in enumerate(update[1:]):
        for previous_step in update[:i+1]:
            if previous_step in rules[step]:
                return 0
    return update[len(update)//2]

def sort_then_score(update: List[int]):
    def insert_in_sorted(_sorted: List[int], to_insert: int):
        for i, already_inserted in enumerate(_sorted):
            if to_insert not in rules[already_inserted]:
                _sorted.insert(i, to_insert)
                return
        _sorted.append(to_insert)
    _sorted = [update[0]]
    for to_insert in update[1:]:
        insert_in_sorted(_sorted, to_insert)
    return _sorted[len(update)//2]

data = sys.stdin.read()
insert_in_rules = True
for line in data.split('\n'):
    if line.strip() == '':
        insert_in_rules = False
    elif insert_in_rules:
        before, after = line.strip().split("|")
        rules[int(before)].append(int(after))
    else:
        updates.append([int(page) for page in line.strip().split(",")])

print("Part 1 is:", sum([score(update) for update in updates]))
print("Part 2 is:", sum([sort_then_score(update) if score(update) == 0 else 0 for update in updates]))
