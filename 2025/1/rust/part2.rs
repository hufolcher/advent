use std::error::Error;
use std::io;

fn main() -> Result<(), Box<dyn Error>> {
    let input = io::read_to_string(io::stdin())?;
    let mut current_dial = 50;
    let mut password = 0;
    for line in input.lines() {
        let (direction, raw_number) = line.split_at(1);
        let number: i32 = raw_number.parse()?;
        for _ in 0..number {
            match direction {
                "L" => current_dial -= 1,
                "R" => current_dial += 1,
                _ => unreachable!(),
            }
            current_dial = (current_dial + 100) % 100;
            if current_dial == 0 {
                password += 1
            }
        }
    }
    println!("Part2 is {:}", password);
    Ok(())
}
