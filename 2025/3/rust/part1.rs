use std::error::Error;
use std::io;

fn main() -> Result<(), Box<dyn Error>> {
    let mut sum: i64 = 0;

    let input = io::read_to_string(io::stdin())?;
    let banks: Vec<String> = input.lines().map(String::from).collect();
    for bank in banks {
        let chars: Vec<char> = bank.chars().collect();
        let digits: Vec<u32> = chars.into_iter().map(|c| c.to_digit(10).unwrap()).collect();

        let mut first = None;
        let mut second = None;
        for (index, digit) in digits.iter().enumerate() {
            if first.is_none() || (index != digits.len() - 1 && digit > first.unwrap()) {
                first = Some(digit);
                second = None;
            } else if second.is_none() || digit > second.unwrap() {
                second = Some(digit);
            }
        }
        sum += (first.unwrap() * 10 + second.unwrap()) as i64;
    }
    println!("Part1 is {:}", sum);
    Ok(())
}
