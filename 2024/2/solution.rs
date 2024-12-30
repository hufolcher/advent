use std::fs;
use std::error::Error;

fn is_safe(first: &i32, following: &i32, decreasing: bool) -> bool {
    (1..4).contains(&(if decreasing {following - first} else {first - following}))
}

fn row_is_increasing_safe(row: &[i32], reverse: bool) -> bool {
    row.into_iter().zip(row[1..].into_iter()).all(|(x,y)| is_safe(x, y, reverse))
}

fn row_is_safe(row: &[i32]) -> bool {
    row_is_increasing_safe(row, true) || row_is_increasing_safe(row, false)
}

fn main() -> Result<(), Box<dyn Error>> {
    let input: String = fs::read_to_string("input.txt")?;
    let mut total1: u32 = 0;
    let mut total2: u32 = 0;
    for line in input.lines() {
        let row : Vec<i32> = line.split(" ").map(|raw| raw.parse().unwrap()).collect();
        if row_is_safe(&row) {
            total1 += 1;
            total2 += 1;
        }
        else {
            for i in 0..row.len() {
                let subrow: Vec<i32> = [&row[..i], &row[i+1..]].concat();
                if row_is_safe(&subrow) {
                    total2 += 1;
                    break
                }
            }
        }
    }
    println!("Part 1 is: {}", total1);
    println!("Part 2 is: {}", total2);
    Ok(())
}