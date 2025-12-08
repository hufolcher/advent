use std::error::Error;
use std::io;
use std::ops::RangeInclusive;

fn into_merged(mut ranges: Vec<RangeInclusive<u64>>) -> Vec<RangeInclusive<u64>> {
    ranges.sort_by_key(|r| *r.start());
    let mut merged = vec![];
    let mut current = ranges[0].clone();
    for next in ranges.into_iter().skip(1) {
        if next.start() <= current.end() {
            let new_end = (current.end()).max(next.end());
            current = *current.start()..=*new_end;
        } else {
            merged.push(current);
            current = next;
        }
    }
    merged.push(current);
    merged
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut fresh_ranges = vec![];
    let input = io::read_to_string(io::stdin())?;
    let mut fresh_data = true;
    for line in input.lines() {
        if line.is_empty() {
            fresh_data = false;
        } else if fresh_data {
            let mut it = line.split('-');
            let start: u64 = it.next().unwrap().parse().unwrap();
            let end: u64 = it.next().unwrap().parse().unwrap();
            fresh_ranges.push(start..=end)
        }
    }
    println!(
        "Part2 is {:?}",
        into_merged(fresh_ranges)
            .iter()
            .map(|r| { *r.end() - *r.start() + 1 })
            .sum::<u64>()
    );
    Ok(())
}
