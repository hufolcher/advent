use std::collections::HashMap;
use std::error::Error;
use std::io;

fn propagate_beam_timeline(
    splitters: &Vec<Vec<bool>>,
    cache: &mut HashMap<(usize, usize), u64>,
    beam_position: usize,
    step: usize,
) -> u64 {
    if let Some(cached) = cache.get(&(beam_position, step)) {
        *cached
    } else {
        if step == splitters.len() {
            return 1;
        }

        let mut new_count = 0;
        if splitters[step][beam_position] {
            for direction in [-1isize, 1].iter() {
                if let Some(cj) = beam_position.checked_add_signed(*direction) {
                    new_count += propagate_beam_timeline(splitters, cache, cj, step + 1);
                }
            }
        } else {
            new_count += propagate_beam_timeline(splitters, cache, beam_position, step + 1);
        }

        cache.insert((beam_position, step), new_count);
        new_count
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = io::read_to_string(io::stdin())?;
    let splitters: Vec<Vec<bool>> = input
        .lines()
        .map(|line| line.chars().map(|c| c == '^').collect())
        .collect();

    let beam_position: usize = input
        .lines()
        .next()
        .unwrap()
        .chars()
        .position(|c| c == 'S')
        .unwrap();

    println!(
        "Part2 is {:?}",
        propagate_beam_timeline(&splitters, &mut HashMap::new(), beam_position, 0)
    );
    Ok(())
}
