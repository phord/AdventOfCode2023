#[allow(unused)]
use yaah::aoc;
#[allow(unused)]
use crate::*;

//------------------------------ PARSE INPUT

fn parse_num(input: &str, part: usize) -> u64 {
    // Find all digits and copy to new array
    let digits = vec!["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"];
    let mut copy = String::new();
    let mut num: Vec<usize> = Vec::new();
    for c in input.chars() {
        copy.push(c);
        if c.is_digit(10) {
            num.push(c as usize - '0' as usize);
        } else {
            if part > 1 {
                for i in 0..digits.len() {
                    if copy.ends_with(digits[i]) {
                        num.push(i);
                    }
                }
            }
        }
    }

    // print!("{input} -> {num:?}\n");
    num[0] as u64 * 10u64 + num[num.len() - 1] as u64
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