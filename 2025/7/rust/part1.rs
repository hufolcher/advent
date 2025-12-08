use std::error::Error;
use std::io;

fn main() -> Result<(), Box<dyn Error>> {
    let mut split_count = 0;

    let input = io::read_to_string(io::stdin())?;
    let splitters_lines: Vec<Vec<bool>> = input
        .lines()
        .map(|line| line.chars().map(|c| c == '^').collect())
        .collect();

    let mut beam: Vec<bool> = input
        .lines()
        .next()
        .unwrap()
        .chars()
        .map(|c| c == 'S')
        .collect();

    for splitters_line in splitters_lines {
        let mut new_beam = vec![false; beam.len()];
        for (j, is_a_splitter_here) in splitters_line.iter().enumerate() {
            if beam[j] {
                if *is_a_splitter_here && beam[j] {
                    split_count += 1;
                    for direction in [-1isize, 1].iter() {
                        if let Some(cj) = j.checked_add_signed(*direction) {
                            new_beam[cj] = true;
                        }
                    }
                } else {
                    new_beam[j] = true;
                }
            }
        }
        beam = new_beam.clone();
    }
    println!("Part1 is {:?}", split_count);
    Ok(())
}
