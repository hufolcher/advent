use std::error::Error;
use std::io;
use std::ops::RangeInclusive;

fn raycast_x_then_y(
    horizontal_borders: &[(u32, RangeInclusive<u32>)],
    vertical_borders: &[(u32, RangeInclusive<u32>)],
    p1: (u32, u32),
    p2: (u32, u32),
) -> bool {
    let (x1, y1) = p1;
    let (x2, y2) = p2;

    let start_x = x1.min(x2);
    let end_x = x1.max(x2);
    for (x, y_range) in vertical_borders {
        if *x > start_x && *x < end_x && y_range.contains(&y1) {
            return false;
        }
    }

    let start_y = y1.min(y2);
    let end_y = y1.max(y2);
    for (y, x_range) in horizontal_borders {
        if *y > start_y && *y < end_y && x_range.contains(&x2) {
            return false;
        }
    }
    true
}

fn area(a: (u32, u32), b: (u32, u32)) -> u64 {
    let width = a.0.abs_diff(b.0) + 1;
    let height = a.1.abs_diff(b.1) + 1;
    width as u64 * height as u64
}

fn main() -> Result<(), Box<dyn Error>> {
    let input: String = io::read_to_string(io::stdin())?;
    let mut red_tiles_positions: Vec<(u32, u32)> = input
        .lines()
        .map(|raw| {
            let mut splitted = raw.split(',').map(|x| x.parse().unwrap());
            (splitted.next().unwrap(), splitted.next().unwrap())
        })
        .collect();
    red_tiles_positions.push(red_tiles_positions[0]);

    let mut vertical_borders: Vec<(u32, RangeInclusive<u32>)> = Vec::new();
    let mut horizontal_borders: Vec<(u32, RangeInclusive<u32>)> = Vec::new();

    for (&(x1, y1), &(x2, y2)) in red_tiles_positions
        .iter()
        .zip(red_tiles_positions.iter().skip(1))
    {
        if x1 == x2 {
            let start = y1.min(y2);
            let end = y1.max(y2);
            vertical_borders.push((x1, start..=end));
        } else if y1 == y2 {
            let start = x1.min(x2);
            let end = x1.max(x2);
            horizontal_borders.push((y1, start..=end));
        }
    }

    vertical_borders.sort_by_key(|(x, r)| (*x, *r.start()));
    horizontal_borders.sort_by_key(|(y, r)| (*y, *r.start()));

    let mut pairs: Vec<_> = red_tiles_positions
        .iter()
        .enumerate()
        .flat_map(|(i, a)| {
            red_tiles_positions[i + 1..]
                .iter()
                .filter(|&&d| {
                    raycast_x_then_y(&horizontal_borders, &vertical_borders, *a, d)
                        && raycast_x_then_y(&horizontal_borders, &vertical_borders, d, *a)
                })
                .map(|&d| area(*a, d))
        })
        .collect();
    pairs.sort_by(|a, b| b.partial_cmp(a).unwrap());

    println!("{:?}", pairs[0]);
    Ok(())
}
