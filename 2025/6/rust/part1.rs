use std::error::Error;
use std::io;

fn main() -> Result<(), Box<dyn Error>> {
    let input = io::read_to_string(io::stdin())?;
    let operations: Vec<Vec<&str>> = input
        .lines()
        .map(|line| line.split_whitespace().collect())
        .collect();

    let (operators, operands_lines) = operations
        .split_last()
        .expect("input must contain at least one line");

    let operands: Vec<Vec<u32>> = operands_lines
        .iter()
        .map(|line| line.iter().map(|v| v.parse::<u32>().unwrap()).collect())
        .collect();

    println!(
        "Part1 is {:?}",
        (0..operators.len())
            .map(|col| match operators[col] {
                "+" => operands.iter().map(|row| row[col] as u64).sum::<u64>(),
                "*" => operands.iter().map(|row| row[col] as u64).product::<u64>(),
                op => panic!("Unknown operator: {}", op),
            })
            .sum::<u64>()
    );
    Ok(())
}
