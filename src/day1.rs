#[allow(unused)]
use yaah::aoc;
#[allow(unused)]
use crate::*;

//------------------------------ PARSE INPUT

fn parse_num_from_str(input: &str, part: usize) -> Option<u64> {
    // Find all digits and copy to new array
    let digits = vec!["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"];

    let c = input.chars().next().unwrap();
    if c.is_digit(10) {
            return Some(c as u64 - '0' as u64);
    } else {
        if part > 1 {
            for i in 0..digits.len() {
                if input.starts_with(digits[i]) {
                    return Some(i as u64);
                }
            }
        }
    }
    return None;
}

#[test]
fn test_numbers() {
    assert_eq!(parse_num_from_str("12345", 1), Some(1));
    assert_eq!(parse_num_from_str("five", 1), None);
    assert_eq!(parse_num_from_str("five", 2), Some(5));
}


fn parse_num(input: &str, part: usize) -> u64 {

    let mut left = 0u64;
    let mut right = 0u64;
    let end = input.len();
    for i in 0..end {
        if let Some(l) = parse_num_from_str(&input[i..], part) {
            left = l;
            break;
        }
    }

    for i in 0..input.len() {
        if let Some(r) = parse_num_from_str(&input[end-i-1..], part) {
            right = r;
            break;
        }
    }

    // print!("{input} -> {num:?}\n");
    left * 10u64 + right
}


fn solve(_input: &'static str, count: usize) -> u64 {
    // Split input into lines
    let mut _input = _input.lines().collect::<Vec<_>>();
    let mut total = 0;
    for line in _input.iter_mut() {
        *line = line.trim();
        let num = parse_num(line, count);
        total += num;
        // print!("{line} = {num}\n");
    }
    total
}

//------------------------------ PART 1

#[aoc(day1, part1)]
fn day1_part1(_input: &'static str) -> u64 {
    solve(_input, 1)
}

#[test]
fn test_day1_part1() {
    assert_eq!(day1_part1(_SAMPLE), _ANS1);
}

//------------------------------ PART 2

#[aoc(day1, part2)]
fn day1_part2(_input: &'static str) -> u64 {
    solve(_input, 2)
}

#[test]
fn test_day1_part2() {
    assert_eq!(day1_part2(_SAMPLE2), _ANS2);
}

//------------------------------ SAMPLE DATA

const _SAMPLE: &str = "1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet";

const _SAMPLE2: &str = "two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen";

const _ANS1: u64 = 142;
const _ANS2: u64 = 281;