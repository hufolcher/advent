use std::collections::{HashMap, HashSet};
use std::error::Error;
use std::io;

fn distance(a: (u32, u32, u32), b: (u32, u32, u32)) -> f32 {
    let dx = a.0 as f32 - b.0 as f32;
    let dy = a.1 as f32 - b.1 as f32;
    let dz = a.2 as f32 - b.2 as f32;
    (dx * dx + dy * dy + dz * dz).sqrt()
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = io::read_to_string(io::stdin())?;
    let boxes: Vec<(u32, u32, u32)> = input
        .lines()
        .map(|raw| {
            let mut splitted = raw.split(',').map(|x| x.parse().unwrap());
            (
                splitted.next().unwrap(),
                splitted.next().unwrap(),
                splitted.next().unwrap(),
            )
        })
        .collect();

    let mut junctions: Vec<_> = boxes
        .iter()
        .enumerate()
        .flat_map(|(i, a)| {
            boxes
                .iter()
                .enumerate()
                .filter_map(move |(j, b)| (i < j).then_some((distance(*a, *b), (i, j))))
        })
        .collect();
    junctions.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());

    let mut circuits: Vec<HashSet<usize>> = (0..boxes.len())
        .map(|i| {
            let mut set = HashSet::new();
            set.insert(i);
            set
        })
        .collect();

    let mut box_to_circuit_index: HashMap<usize, usize> =
        (0..boxes.len()).map(|i| (i, i)).collect();
    for &(_, (i, j)) in &junctions {
        let i_circuit_index = box_to_circuit_index[&i];
        let j_circuit_index = box_to_circuit_index[&j];
        if i_circuit_index == j_circuit_index {
            continue;
        }
        for j_circuit_box in std::mem::take(&mut circuits[j_circuit_index]) {
            circuits[i_circuit_index].insert(j_circuit_box);
            box_to_circuit_index.insert(j_circuit_box, i_circuit_index);
        }
        if circuits.iter().filter(|set| !set.is_empty()).count() == 1 {
            println!("Part2 is {:?}", boxes[i].0 as u64 * boxes[j].0 as u64);
            break;
        }
    }
    Ok(())
}
