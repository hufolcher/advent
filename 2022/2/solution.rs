use std::collections::HashMap;
use std::error::Error;
use std::io;

fn main() -> Result<(), Box<dyn Error>> {
    let input = io::read_to_string(io::stdin())?;
    let round_to_score_part1 = HashMap::from([
        ('A', HashMap::from([('X', 4), ('Y', 8), ('Z', 3)])),
        ('B', HashMap::from([('X', 1), ('Y', 5), ('Z', 9)])),
        ('C', HashMap::from([('X', 7), ('Y', 2), ('Z', 6)])),
    ]);
    let round_to_score_part2 = HashMap::from([
        ('A', HashMap::from([('X', 3), ('Y', 4), ('Z', 8)])),
        ('B', HashMap::from([('X', 1), ('Y', 5), ('Z', 9)])),
        ('C', HashMap::from([('X', 2), ('Y', 6), ('Z', 7)])),
    ]);
    let mut score_part1: u32 = 0;
    let mut score_part2: u32 = 0;
    for line in input.lines() {
        let parts: Vec<&str> = line.split(" ").collect();
        let first: char = parts[0].parse()?;
        let second: char = parts[1].parse()?;
        score_part1 += round_to_score_part1
            .get(&first)
            .unwrap()
            .get(&second)
            .unwrap();
        score_part2 += round_to_score_part2
            .get(&first)
            .unwrap()
            .get(&second)
            .unwrap();
    }
    println!(" {}", score_part1);
    println!("Part2 is: {}", score_part2);
    Ok(())
}
