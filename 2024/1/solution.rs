use std::fs;
use std::error::Error;
use std::collections::HashMap;

fn main() -> Result<(), Box<dyn Error>> {
    let input: String = fs::read_to_string("input.txt")?;
    let mut left_vect: Vec<i32> = Vec::new();
    let mut right_vect: Vec<i32> = Vec::new();
    let mut right_vec_appearances: HashMap<i32,i32> = HashMap::new();

    for line in input.lines() {
        let parts : Vec<&str> = line.split("   ").collect();
        let left: i32 = parts[0].parse()?;
        let right: i32 = parts[1].parse()?;
        left_vect.push(left);
        right_vect.push(right);
        let count = right_vec_appearances.entry(right).or_insert(0);
        *count +=1;
    }
    left_vect.sort();
    right_vect.sort();
    let total1: i32 = left_vect.iter().zip(right_vect.iter()).map(|(left, right)| (left - right).abs()).sum();
    let total2: i32 = left_vect.iter().map(|left| *right_vec_appearances.entry(*left).or_insert(0) * left).sum();
    println!("Part 1 is: {}", total1);
    println!("Part 2 is: {:?}", total2);
    Ok(())
}