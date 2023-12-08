use yaah::{aoc_lib, aoc_year};
use std::str;

mod day1;
mod day2;
mod day3;
mod day4;
// mod day5;
// mod day6;
mod day7;
// mod day8;
// mod day9;
// mod day10;
// mod day11;
// mod day12;
// mod day13;
// mod day14;
// mod day15;
// mod day16;
// mod day17;
// mod day18;
// mod day19;
// mod day20;
// mod day21;
// mod day22;
// mod day23;
// mod day24;
// mod day25;

aoc_year!(2023);
aoc_lib!(with_benchmarks);

//______________________________________________________
//                               GENERIC INPUT SPLITTERS

// Split a string containing multiple lines into a vector of &[u8], one per line
#[allow(unused)]
pub fn split_to_lines(_input: &'static str) -> Vec<&[u8]> {
    _input
        .lines()
        .map(|x| x.as_bytes())
        .collect::<Vec<&[u8]>>()
}

// Split a string on any delimiter; return vector of str
#[allow(unused)]
pub fn split_on(_input: &'static str, delim: &'static str) -> Vec<&'static str> {
    _input
        .split(delim)
        .collect::<Vec<&str>>()
}


// Split a string containing multiple lines into a vector of vectors of words broken on whitespace
#[allow(unused)]
pub fn split_to_words(_input: &'static str) -> Vec<Vec<&[u8]>> {
    _input
        .lines()
        .map(|s| s.split_whitespace()
                        .map(|x| x.as_bytes())
                        .collect())
        .collect::<Vec<Vec<&[u8]>>>()
}

// Split a string containing multiple lines into a vector &[u8]
#[allow(unused)]
pub fn split_to_byte_words(_input: &'static str) -> Vec<Vec<&[u8]>> {
    let foo = split_to_lines(_input);
    let mut bar = Vec::new();
    for line in foo {
        let mut nl = Vec::new();
        for i in 0..line.len() {
            let s = &line[i..i+1];
            nl.push(s);
        }
        bar.push(nl);
    }
    bar
}

// Split a string containing single integer values into a Vec<u64>
#[allow(unused)]
pub fn split_to_ints(_input: &'static str) -> Vec<u64> {
    _input.lines()
        .map(|s| s.parse::<u64>().unwrap())
        .collect::<Vec<u64>>()
}

#[allow(unused)]
pub fn group_between<'a>(inp: Vec<&'a[u8]>, delim: &'static str) -> Vec<Vec<&'a[u8]>> {
    let mut out = Vec::new();

    let mut group = Vec::new();
    for line in inp {
        let s = as_str(&line);
        if s == delim {
            out.push(group.clone());
            group.clear();
        } else {
            group.push(line);
        }
    }
    out.push(group.clone());
    out
}

//______________________________________________________
//                                               PARSERS

#[allow(unused)]
fn as_str(inp: &[u8]) -> &str {
    let s = str::from_utf8(inp).expect("invalid utf8 bytes");
    s
}

// Parse first word up until whitespace.
// Return first word and rest of string starting from the whitespace
#[allow(unused)]
fn parse_word(inp: &str, delim: char) -> (&str, &str) {
    let mut end = 0;
    for c in inp.chars() {
        if c == delim {
            break;
        }
        end += 1;
    }
    inp.split_at(end)
}

// Skip first word up until whitespace.
#[allow(unused)]
fn skip_word(inp: &str) -> &str {
    let inp = skip_ws(inp);
    let (a,b) = parse_word(inp, ' ');
    b
}

// Skip whitespace
#[allow(unused)]
fn skip_ws(inp: &str) -> &str {
    let mut end = 0;
    for c in inp.chars() {
        if !c.is_whitespace() {
            break;
        }
        end += 1;
    }
    inp.split_at(end).1
}

// Parse a number from a string
#[allow(unused)]
fn parse_num(inp: &str) -> (usize, &str) {
    let inp = skip_ws(inp);
    let mut end = 0;
    for c in inp.chars() {
        if !c.is_digit(10) {
            break;
        }
        end += 1;
    }
    let num = inp.split_at(end).0.parse::<usize>().unwrap();
    (num, skip_ws(inp.split_at(end).1))
}

#[allow(unused)]
fn parse_u64(inp: &[u8]) -> u64 {
    let x = as_str(inp).parse::<u64>();
    assert!(x.is_ok(), "not a number: '{}'", as_str(inp));
    x.unwrap()
}

// Convert a binary string to a u64 value.
#[allow(unused)]
fn parse_binary(s: &[u8]) -> u64 {
    let mut res = 0;
    for c in s {
        res *= 2;
        if *c == b'1' { res += 1; }
    }
    res
}

//______________________________________________________
//                                           GRID XFORMS

// Transpose a grid of byte-strings
// ** All rows must have same width.
// FIXME: Remove the Clone requirement
#[allow(unused)]
fn transpose<T: Clone>(grid: Vec<Vec<T>>) -> Vec<Vec<T>> {
    let height = grid[0].len();
    let mut new_grid = vec![vec![]; height];

    for line in grid.into_iter() {
        for (x, cell) in line.into_iter().enumerate() {
            new_grid[x].push(cell);
        }
    }
    new_grid
}

// Rotate a grid of byte-strings +90 degrees clockwise
// ** All rows must have same width.
#[allow(unused)]
fn rotate<T: Clone>(v: Vec<Vec<T>>) -> Vec<Vec<T>> {
    assert!(!v.is_empty());
    let len = v[0].len();
    let mut iters: Vec<_> = v.into_iter().map(|n| n.into_iter()).collect();
    (0..len)
        .map(|_| {
            iters
                .iter_mut()
                .map(|n| n.next().unwrap())
                .rev()
                .collect::<Vec<T>>()
        })
        .collect()
}

// Mirror a grid around vertical axis
#[allow(unused)]
fn mirror_vertical<T>(grid: Vec<Vec<T>>) -> Vec<Vec<T>> {
    grid.into_iter().map(|row| row.into_iter().rev().collect()).collect()
}

// Mirror a grid around horizontal axis
#[allow(unused)]
fn mirror_horizontal<T:Copy>(grid: Vec<Vec<T>>) -> Vec<Vec<T>> {
    let mut new_grid = grid.clone();
    new_grid.reverse();
    new_grid
}

#[allow(unused)]
const SAMPLE: &str = "forward 5
down 5
forward 8
up 3
down 8
forward 2";

#[test]
fn test_transpose() {
    let moves = split_to_words(SAMPLE);
    print_grid(&moves);
    let trans1 = transpose(moves);
    print_grid(&trans1);
    let trans2 = transpose(trans1);
    let orig = split_to_words(SAMPLE);
    assert_eq!(orig, trans2);
}

#[test]
fn test_rotate() {
    let moves = split_to_words(SAMPLE);
    print_grid(&moves);
    let rot1 = rotate(moves);
    print_grid(&rot1);
    let rot2 = rotate(rot1);
    print_grid(&rot2);
    let rot3 = rotate(rot2);
    print_grid(&rot3);
    let rot4 = rotate(rot3);
    let orig = split_to_words(SAMPLE);
    assert_eq!(orig, rot4);
}

#[allow(unused)]
const IMAGE: &str = "foo..bar
........
.X....X.
........
...XX...
X.......
.xxxxx..
......xx";

#[test]
fn test_split_byte_words() {
    let moves = split_to_byte_words(IMAGE);
    print_grid(&moves);
    let rot1 = rotate(moves);
    print_grid(&rot1);
    let rot2 = rotate(rot1);
    print_grid(&rot2);
    let rot3 = rotate(rot2);
    print_grid(&rot3);
    let rot4 = rotate(rot3);
    let orig = split_to_byte_words(IMAGE);
    assert_eq!(orig, rot4);
}

#[test]
fn test_mirror() {
    let moves = split_to_byte_words(IMAGE);
    print_grid(&moves);
    let rot1 = mirror_vertical(moves);
    print_grid(&rot1);
    let rot2 = mirror_horizontal(rot1);
    print_grid(&rot2);
    let rot3 = mirror_vertical(rot2);
    print_grid(&rot3);
    let rot4 = mirror_horizontal(rot3);
    let orig = split_to_byte_words(IMAGE);
    assert_eq!(orig, rot4);
}

//______________________________________________________
//                                               HELPERS

// Print a grid of [u8] as strings
#[allow(unused)]
fn print_grid(grid: &Vec<Vec<&[u8]>>) {
    for (y, line) in grid.iter().enumerate() {
        for (x, cell) in line.iter().enumerate() {
            print!("{} ", as_str(cell))
        }
        println!("");
    }
}