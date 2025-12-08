use std::error::Error;
use std::io;

fn main() -> Result<(), Box<dyn Error>> {
    let mut sum: u64 = 0;
    let input = io::read_to_string(io::stdin())?;

    let mut lines: Vec<String> = input.lines().map(|l| l.to_string()).collect();
    let width = lines.iter().map(|line| line.len()).max().unwrap_or(0);
    for line in &mut lines {
        if line.len() < width {
            line.push_str(&" ".repeat(width - line.len()));
        }
    }
    let operations: Vec<Vec<char>> = lines
        .into_iter()
        .map(|line| line.chars().rev().collect())
        .collect();

    let mut operands: Vec<u64> = vec![];
    for i in 0..width {
        let mut values: Vec<char> = operations.iter().map(|row| row[i]).collect();
        let operator = values.pop().unwrap();
        if let Ok(parsed) = values
            .iter()
            .filter(|c| !c.is_whitespace())
            .collect::<String>()
            .parse::<u64>()
        {
            operands.push(parsed);
        }
        if operator == '+' {
            sum += operands.iter().sum::<u64>();
            operands.clear();
        } else if operator == '*' {
            sum += operands.iter().product::<u64>();
            operands.clear();
        }
    }

    println!("{:}", sum);
    Ok(())
}
