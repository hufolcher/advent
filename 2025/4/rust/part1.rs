use std::error::Error;
use std::io;

const DIRS: [(isize, isize); 8] = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
];

fn count_surrounding(diagram: &Vec<Vec<bool>>, i: usize, j: usize) -> usize {
    DIRS.iter()
        .filter_map(|(di, dj)| {
            let ni = i.checked_add_signed(*di)?;
            let nj = j.checked_add_signed(*dj)?;
            diagram.get(ni)?.get(nj)
        })
        .filter(|&&b| b)
        .count()
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = io::read_to_string(io::stdin())?;
    let rolls: Vec<Vec<bool>> = input
        .lines()
        .map(|line| line.chars().map(|c| c == '@').collect())
        .collect();

    println!(
        "Part1 is {:?}",
        (0..rolls.len())
            .flat_map(|i| (0..rolls[i].len()).map(move |j| (i, j)))
            .filter(|&(i, j)| (rolls[i][j] && count_surrounding(&rolls, i, j) < 4))
            .count()
    );
    Ok(())
}
