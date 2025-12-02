use std::error::Error;
use std::io;

fn main() -> Result<(), Box<dyn Error>> {
    let input = io::read_to_string(io::stdin())?;
    let mut current_dial = 50;
    let mut password = 0;
    for line in input.lines() {
        let (direction, raw_number) = line.split_at(1);
        let number: i32 = raw_number.parse()?;
        match direction {
            "L" => {
                current_dial = ((current_dial as i32 - number) % 100 + 100) % 100;
            }
            "R" => {
                current_dial = ((current_dial as i32 + number) % 100 + 100) % 100;
            }
            _ => unreachable!(),
        }
        if current_dial == 0 {
            password += 1
        }
    }
    println!("Part1 is {:}", password);
    Ok(())
}
