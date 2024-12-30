use std::fs;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let input: String = fs::read_to_string("input.txt")?;
    let mut total_weight_carried: Vec<u32> = Vec::new();
    total_weight_carried.push(0);

    for line in input.lines() {
        match line {
            "" => total_weight_carried.push(0),
            int_str => *total_weight_carried.last_mut().unwrap() += int_str.parse::<u32>()?,
        }
    }
    total_weight_carried.sort();
    println!("Part1 is: {}", total_weight_carried.last().unwrap());
    println!("Part2 is: {}", total_weight_carried.iter().rev().take(3).sum::<u32>());
    Ok(())
}