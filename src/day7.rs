#[allow(unused)]
use yaah::aoc;
use itertools::Itertools;

#[derive(Debug, Eq, PartialEq, PartialOrd, Ord)]
struct Hand <'a> {
    value: Vec<usize>,
    cards: &'a str,
    bid: usize,
}

impl <'a> Hand<'_> {
    fn score(cards: &'a str, _part: usize) -> Vec<usize> {
        // TODO: for part2, add count for J into count for highest non-J card
        let mut counts = cards.chars().counts();
        let jokers = if _part == 2 {
            let jokers = *counts.get(&'J').unwrap_or(&0);
            if counts.len() > 1 {
                counts.remove(&'J');
                jokers
            } else { 0 }
        } else {
            0
        };
        let c = counts.iter().map(|(k, v)| *v).collect_vec();
        // reverse sort c
        let mut c = c.iter().cloned().sorted().rev().collect_vec();
        c[0] += jokers;
        c
    }

    fn new(cards: &str, bid: usize, _part: usize) -> Hand {
        let value = Self::score(cards, _part);
        let v2:Vec<usize> = cards.chars().map(|c| {
            match c {
                'A' => 14,
                'K' => 13,
                'Q' => 12,
                'J' => if _part == 1 {11} else { 1 },
                'T' => 10,
                _ => c.to_digit(10).unwrap() as usize,
            }
        }).collect();
        let value = value.iter().chain(v2.iter()).map(|x| *x).collect_vec();
        Hand { value, cards, bid }
    }
}

fn get_games(_input: &'static str, _part: usize) -> Vec<Hand> {
    _input.lines().map(|line| {
        let mut parts = line.split_whitespace();
        let cards = parts.next().unwrap();
        let bid = parts.next().unwrap().parse::<usize>().unwrap();
        Hand::new( cards, bid , _part)
    }).collect()
}

fn solve(_input: &'static str, _part: usize) -> usize {
    let games = get_games(_input, _part);
    // sort games
    let mut total = 0;
    for (i, game) in games.iter().sorted().enumerate() {
        total += (i+1) * game.bid;
        // println!("{}: {:?}", i, game);
    }
    total
}

//------------------------------ PART 1

#[allow(unused)]
#[aoc(day7, part1)]
fn day7_part1(_input: &'static str) -> usize {
    let ans = solve(_input, 1);
    assert_eq!(ans, 251806792);
    ans
}

#[test]
fn test_day7_part1() {
    assert_eq!(solve(_SAMPLE, 1), _ANS1);
}

//------------------------------ PART 2

#[allow(unused)]
#[aoc(day7, part2)]
fn day7_part2(_input: &'static str) -> usize {
    let ans = solve(_input, 2);
    assert_eq!(ans, 252113488);
    ans
}

#[test]
fn test_day7_part2() {
    assert_eq!(solve(_SAMPLE, 2), _ANS2);
}

//------------------------------ SAMPLE DATA

const _SAMPLE: &str = "32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483";

const _ANS1: usize = 6440;
const _ANS2: usize = 5905;