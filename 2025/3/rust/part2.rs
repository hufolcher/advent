use std::error::Error;
use std::io;

const BATTERIES_TO_TURN_ON_PER_BANK: usize = 12;

fn main() -> Result<(), Box<dyn Error>> {
    let mut sum: i64 = 0;

    let input = io::read_to_string(io::stdin())?;
    let banks: Vec<String> = input.lines().map(String::from).collect();
    for bank in banks {
        let chars: Vec<char> = bank.chars().collect();
        let digits: Vec<u32> = chars.into_iter().map(|c| c.to_digit(10).unwrap()).collect();
        let bank_lenght = digits.len();

        let mut candidates = [None; BATTERIES_TO_TURN_ON_PER_BANK];
        for (index, digit) in digits.into_iter().enumerate() {
            for rank in 0..BATTERIES_TO_TURN_ON_PER_BANK {
                if candidates[rank].is_none()
                    || (index < bank_lenght - (BATTERIES_TO_TURN_ON_PER_BANK - rank - 1)
                        && digit > candidates[rank].unwrap())
                {
                    candidates[rank] = Some(digit);
                    for following_rank in (rank + 1)..BATTERIES_TO_TURN_ON_PER_BANK {
                        candidates[following_rank] = None;
                    }
                    break;
                }
            }
        }
        sum += candidates
            .iter()
            .map(|&d| d.unwrap())
            .fold(0, |acc, d| acc * 10 + d as i64);
    }
    println!("Part2 is {:}", sum);
    Ok(())
}
