use std::fs;
use std::error::Error;
use std::collections::HashMap;

fn main() -> Result<(), Box<dyn Error>> {
    let input: String = fs::read_to_string("input.txt")?;
    for line in input.lines() {
        let mid_index = line.len() / 2;
        for (c,a) in line[..mid_index].chars().zip(line[mid_index..].chars()) {
            println!("{:?} {:?}", c, a);
        }
    }
    // println!("Part1 is: {}", score_part1);
    // println!("Part2 is: {}", score_part2);
    Ok(())
}