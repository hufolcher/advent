use std::error::Error;
use std::io;

fn main() -> Result<(), Box<dyn Error>> {
    let input = io::read_to_string(io::stdin())?;
    let mut sum: i64 = 0;
    for range in input.lines().next().unwrap().split(',') {
        let mut splitted = range.split('-');
        let start: i64 = splitted.next().unwrap().parse()?;
        let end: i64 = splitted.next().unwrap().parse()?;

        for candidate in start..=end {
            let candidate_as_string = candidate.to_string();
            if candidate_as_string.len() % 2 == 0 {
                let (left, right) = candidate_as_string.split_at(candidate_as_string.len() / 2);
                if left == right {
                    sum += candidate;
                }
            }
        }
    }
    println!("Part1 is {:}", sum);
    Ok(())
}
