use std::error::Error;
use std::io::{self, Read};
use std::collections::HashMap;

#[derive(Debug)]
enum Direction {
    Top = (-1, 0)
    Right = (0, 1)
    Bottom = (1, 0)
    Left = (0, -1)
}
impl Direction {
    fn next(&self) -> Self {
        match self {
            Direction::Top => Direction::Right,
            Direction::Right => Direction::Bottom,
            Direction::Bottom => Direction::Left,
            Direction::Left => Direction::Top,
        }
    }
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
