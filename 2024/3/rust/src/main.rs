extern crate regex;
use regex::Regex;

use std::error::Error;
use std::io::{self, Read};

fn main() -> Result<(), Box<dyn Error>> {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).expect("Failed to read from stdin");

    let mut total1: i32 = 0;
    let mut total2: i32 = 0;

    let enabled_sequences: Vec<&str> = input.split("do()").collect();
    let re = Regex::new(r"mul\((\d+),(\d+)\)").unwrap();

    for sequence in enabled_sequences {
        let true_enabled: Vec<&str> = sequence.split("don't()").collect();
        for (i, splitted) in true_enabled.iter().enumerate() {
            for _match in re.captures_iter(splitted) {
                let increment: i32 = [_match.get(1), _match.get(2)].map(|x| x.unwrap().as_str().parse::<i32>().unwrap()).iter().product::<i32>();
                total1 += increment;
                if i == 0 {
                    total2 += increment;
                }
            }
        }
    }
    println!("Part 1 is: {}", total1);
    println!("Part 2 is: {}", total2);
    Ok(())
}