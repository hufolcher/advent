use std::fs;
use std::error::Error;
use std::collections::HashMap;

fn main() -> Result<(), Box<dyn Error>> {
    let input: String = fs::read_to_string("input.txt")?;
    let mut left_vect: Vec<i32> = Vec::new();
    let mut right_vect: Vec<i32> = Vec::new();
    let mut right_vect_appearances: HashMap<i32,i32> = HashMap::new();

    for line in input.lines() {
        let parts : Vec<&str> = line.split("   ").collect();
        left_vect.push(parts[0].parse()?);
        right_vect.push(parts[1].parse()?);
        *right_vect_appearances.entry(parts[1].parse()?).or_insert(0) += 1;
    }
    left_vect.sort();
    right_vect.sort();

    let total1: i32 = left_vect.iter().zip(right_vect.iter()).map(|(left, right)| (left - right).abs()).sum();
    let total2: i32 = left_vect.iter().map(|left| *right_vect_appearances.entry(*left).or_insert(0) * left).sum();
    println!("Part 1 is: {}", total1);
    println!("Part 2 is: {}", total2);
    Ok(())
}