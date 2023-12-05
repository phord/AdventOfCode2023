#[allow(unused)]
use yaah::aoc;
#[allow(unused)]
use crate::*;

//------------------------------ PARSE INPUT

#[derive(Copy, Clone)]
struct Number {
    num: usize,
    row: usize,
    start: usize,
    end: usize,
}

// import debug print for Number
#[allow(unused)]
use std::fmt::Debug;
impl Debug for Number {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{num} ({row},{start}-{end})", num=self.num, row=self.row, start=self.start, end=self.end)
    }
}


fn parse_nums(_input: &'static str) -> Vec<Number> {
    let mut num: Option<Number> = None;
    let mut nums: Vec<Number> = Vec::new();

    let mut row = 0;
    for line in _input.lines() {
        let mut start = 0;
        for c in line.chars() {
            if c.is_digit(10) {
                if num.is_none() {
                    num = Some(Number { num: (c.to_digit(10)).unwrap() as usize, row, start, end: start });
                } else {
                    num.as_mut().unwrap().num *= 10;
                    num.as_mut().unwrap().num += (c.to_digit(10)).unwrap() as usize;
                    num.as_mut().unwrap().end = start;
                }
            } else {
                if num.is_some() {
                    nums.push(num.unwrap());
                    num = None;
                }
            }
            start += 1;
        }
        row += 1;
    }
    nums
}

fn parse_syms(_input: &'static str) -> Vec<(usize,usize)> {
    let mut syms: Vec<(usize,usize)> = Vec::new();

    let mut row = 0;
    for line in _input.lines() {
        let mut col = 0;
        for c in line.chars() {
            if !c.is_digit(10) && c != '.' {
                syms.push((row, col));
            }
            col += 1;
        }
        row += 1;
    }
    syms
}

fn parse_gears(_input: &'static str) -> Vec<(usize,usize)> {
    let mut syms: Vec<(usize,usize)> = Vec::new();

    let mut row = 0;
    for line in _input.lines() {
        let mut col = 0;
        for c in line.chars() {
            if c == '*' {
                syms.push((row, col));
            }
            col += 1;
        }
        row += 1;
    }
    syms
}

fn touches(num: &Number, sym: &(usize,usize)) -> bool {
    let (y, x) = sym;
    let (y, x) = (*y as i32, *x as i32);
    let (row, start, end) = (num.row as i32, num.start as i32, num.end as i32);

    if row == y {
        return x == start-1 || x == end+1
    }

    if (row - y).abs() != 1 {return false }
    if start > x+1 {return false }
    if end < x-1 {return false }
    return true
}

//------------------------------ SOLVE

fn solve1(_input: &'static str) -> usize {
    let nums = parse_nums(&_input);
    let syms = parse_syms(_input);

    let mut total = 0;
    for num in nums.iter() {
        for sym in syms.iter() {
            if touches(num, sym) {
                total += num.num;
                // println!("{} touches {:?}", num.num, sym);
                break;
            }
        }
    }
    total
}

fn solve2(_input: &'static str) -> usize {
    let nums = parse_nums(&_input);
    let gears = parse_gears(_input);

    let mut total = 0;
    for gear in gears.iter() {
        let mut touched: Vec<Number> = Vec::new();
        for num in nums.iter() {
            if touches(num, gear) {
                touched.push(*num);
            }
        }
        if touched.len() == 2 {
            total += touched[0].num * touched[1].num;
        }
    }
    total
}

//------------------------------ PART 1

#[allow(unused)]
#[aoc(day3, part1)]
fn day3_part1(_input: &'static str) -> usize {
    let ans = solve1(_input);
    assert_eq!(ans, 528819);
    ans
}

#[test]
fn test_day3_part1() {
    assert_eq!(solve1(_SAMPLE), _ANS1);
}

//------------------------------ PART 2

#[allow(unused)]
#[aoc(day3, part2)]
fn day3_part2(_input: &'static str) -> usize {
    let ans = solve2(_input);
    assert_eq!(ans, 80403602);
    ans
}

#[test]
fn test_day3_part2() {
    assert_eq!(solve2(_SAMPLE), _ANS2);
}

//------------------------------ SAMPLE DATA

const _SAMPLE: &str = "467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..";

const _ANS1: usize = 4361;
const _ANS2: usize = 467835;