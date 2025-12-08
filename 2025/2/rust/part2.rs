use std::error::Error;
use std::io;

fn sorted_dividers(n: usize) -> Vec<usize> {
    let mut result = Vec::new();
    let mut i = 1;
    while i * i <= n {
        if n % i == 0 {
            result.push(i);
            if i != n / i {
                result.push(n / i);
            }
        }
        i += 1;
    }
    result.sort_unstable();
    result
}

fn split_equal(s: &str, divider: usize) -> Vec<&str> {
    let len = s.len();
    let step = len / divider;
    (0..divider).map(|i| &s[i * step..(i + 1) * step]).collect()
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = io::read_to_string(io::stdin())?;
    let mut sum: i64 = 0;
    for range in input.lines().next().unwrap().split(',') {
        let mut splitted = range.split('-');
        let start: i64 = splitted.next().unwrap().parse()?;
        let end: i64 = splitted.next().unwrap().parse()?;

        for candidate in start..=end {
            let candidate_as_string = candidate.to_string();
            for divider in sorted_dividers(candidate_as_string.len()).into_iter().rev() {
                if divider != 1 {
                    let parts = split_equal(&candidate_as_string, divider);
                    if parts.iter().all(|p| *p == parts[0]) {
                        sum += candidate;
                        break;
                    }
                }
            }
        }
    }
    println!("Part2 is {:}", sum);
    Ok(())
}
