use std::error::Error;
use std::io::{self, Read};
use std::collections::HashMap;

fn populate_rules(rules: &mut HashMap<u16, Vec<u16>>, raw: &str) {
    match raw.split_once('|') {
        Some((first, second)) =>
            match (first.parse(), second.parse()) {
                (Ok(before), Ok(after)) => rules.entry(before).or_insert(Vec::new()).push(after),
                _ => (),
            }
        None => (),
    }
}

fn score(update: &Vec<u16>, rules: &HashMap<u16, Vec<u16>>) -> u16 {
    for (i, step) in update[1..].iter().enumerate() {
        for previous_step in update[..i+1].iter() {
            match rules.get(step) {
                Some(after) if after.contains(previous_step) => return 0,
                _ => (),
            }
        }
    }
    return update[update.len()/2]
}

fn sort_then_score(update: &Vec<u16>, rules: &HashMap<u16, Vec<u16>>) -> u16 {
    fn insert_in_sorted(_sorted: &mut Vec<u16>, to_insert: &u16, rules: &HashMap<u16, Vec<u16>>) {
        for (i, already_inserted) in _sorted.into_iter().enumerate() {
            match rules.get(already_inserted) {
                Some(after) if after.contains(to_insert) => continue,
                _ => {_sorted.insert(i, *to_insert); return},
            }
        }
        _sorted.push(*to_insert);
    }
    let mut _sorted = vec![update[0]];
    update[1..].iter().for_each(|to_insert| insert_in_sorted(&mut _sorted, to_insert, rules));
    return _sorted[update.len()/2]
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut rules: HashMap<u16, Vec<u16>> = HashMap::new();
    let mut updates: Vec<Vec<u16>> = Vec::new();

    let mut input = String::new();
    io::stdin().read_to_string(&mut input).expect("Failed to read from stdin");

    let mut insert_in_rules: bool = true;
    for line in input.lines() {
        match line {
            "" => insert_in_rules = false,
            to_be_parsed  => {
                if insert_in_rules {
                    populate_rules(&mut rules, to_be_parsed)
                }
                else {
                    updates.push(to_be_parsed.split(',').map(|s| s.parse::<u16>()).filter_map(Result::ok).collect())
                }
            },
        }
    }
    println!("Part 1 is: {}", updates.iter().map(|update| score(update, &rules)).sum::<u16>());
    println!("Part 2 is: {}", updates.iter().map(|update| {if score(update, &rules) == 0 {sort_then_score(update, &rules)} else {0}}).sum::<u16>());
    Ok(())
}
