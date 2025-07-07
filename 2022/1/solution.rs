use std::error::Error;
use std::io::{self, Read};

fn main() -> Result<(), Box<dyn Error>> {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input)?;

    let mut total_weight_carried: Vec<u32> = vec![0];

    for line in input.lines() {
        match line {
            "" => total_weight_carried.push(0),
            int_str => *total_weight_carried.last_mut().unwrap() += int_str.parse::<u32>()?,
        }
    }

    total_weight_carried.sort();
    println!("Part1 is: {}", total_weight_carried.last().unwrap());
    println!(
        "Part2 is: {}",
        total_weight_carried.iter().rev().take(3).sum::<u32>()
    );

    Ok(())
}
