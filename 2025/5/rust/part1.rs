use std::error::Error;
use std::io;

fn main() -> Result<(), Box<dyn Error>> {
    let mut sum: usize = 0;
    let mut fresh_ranges = vec![];
    let input = io::read_to_string(io::stdin())?;
    let mut fresh_data = true;
    for line in input.lines() {
        if line == "" {
            fresh_data = false;
        } else {
            if fresh_data {
                let mut it = line.split('-');
                let start: u64 = it.next().unwrap().parse().unwrap();
                let end: u64 = it.next().unwrap().parse().unwrap();
                fresh_ranges.push(start..=end.into())
            } else {
                let ingredient: u64 = line.parse().unwrap();
                for interval in &fresh_ranges {
                    if interval.contains(&ingredient) {
                        sum += 1;
                        break;
                    }
                }
            }
        }
    }
    println!("Part1 is {:?}", sum);
    Ok(())
}
