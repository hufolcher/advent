use std::io;

fn main() {
    let input = io::read_to_string(io::stdin()).unwrap();
    println!("{}", input.len());
}
