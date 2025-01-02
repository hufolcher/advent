use std::error::Error;
use std::io::{self, Read};

fn get_with_offset(data: &Vec<Vec<char>>, i: usize, j: usize, offset_i: isize, offset_j: isize) -> Option<char> {
    match (i.checked_add_signed(offset_i), j.checked_add_signed(offset_j)) {
        (Some(current_i), Some(current_j)) if {current_i < data.len() && current_j < data[current_i].len()} => return Some(data[current_i][current_j]),
        _ => return None
    }
}

fn part1_pattern_from_direction(data: &Vec<Vec<char>>, i: usize, j: usize, direction: (isize, isize)) -> bool{
    let (direction_i, direction_j) = direction;
    for (scalar, expected) in (1isize..).zip(['M','A','S']) {
        match get_with_offset(data, i, j, direction_i * scalar, direction_j * scalar) {
            Some(distant_char) if {distant_char == expected} => continue,
            _ => return false,
        };
    }
    return true;
}

fn part2_pattern(data: &Vec<Vec<char>>, i: usize, j: usize) -> bool{
    fn is_valid_diagonal(first: char, second: char) -> bool{
        match (first, second) {
            ('M','S') => true,
            ('S','M') => true,
            _ => false
        }
    }
    let corners: [(isize, isize); 4] = [(-1, -1), (1, 1), (-1, 1), (1, -1)];
    match corners.iter().map(|(offset_i, offset_j)| get_with_offset(data, i, j, *offset_i, *offset_j)).collect::<Vec<Option<char>>>().as_slice() {
        [Some(tl), Some(br), Some(tr), Some(bl)] if {is_valid_diagonal(*bl,*tr) && is_valid_diagonal(*br,*tl)}=> true,
        _ => return false
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let mut total1: u16 = 0;
    let mut total2: u16 = 0;
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).expect("Failed to read from stdin");
    let data: Vec<Vec<char>> = input.lines().collect::<Vec<&str>>().into_iter().map(|line| line.chars().collect::<Vec<char>>()).collect();
    for i in 0usize..data.len() {
        for j in 0usize..data[i].len() {
            match data[i][j] {
                'X' => total1 += [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)].into_iter().map(|direction| part1_pattern_from_direction(&data, i ,j, direction) as u16).sum::<u16>(),
                'A' if {part2_pattern(&data, i, j)} => total2 += 1,
                _ => (),
            }
        }
    }
    println!("Part 1 is: {}", total1);
    println!("Part 2 is: {}", total2);
    Ok(())
}