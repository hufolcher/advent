use std::error::Error;
use std::io;

fn area(a: (u32, u32), b: (u32, u32)) -> u64 {
    let width = a.0.abs_diff(b.0) + 1;
    let height = a.1.abs_diff(b.1) + 1;
    width as u64 * height as u64
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = io::read_to_string(io::stdin())?;
    let red_tiles: Vec<(u32, u32)> = input
        .lines()
        .map(|raw| {
            let mut splitted = raw.split(',').map(|x| x.parse().unwrap());
            (splitted.next().unwrap(), splitted.next().unwrap())
        })
        .collect();

    let mut pairs: Vec<_> = red_tiles
        .iter()
        .enumerate()
        .flat_map(|(i, a)| {
            red_tiles
                .iter()
                .enumerate()
                .filter_map(move |(j, b)| (i < j).then_some((area(*a, *b), (i, j))))
        })
        .collect();
    pairs.sort_by(|a, b| b.0.partial_cmp(&a.0).unwrap());
    println!("{:?}", pairs[0].0);
    Ok(())
}
