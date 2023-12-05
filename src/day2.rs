#[allow(unused)]
use yaah::aoc;
#[allow(unused)]
use crate::*;

//------------------------------ PARSE INPUT

#[derive(Copy, Clone, Debug)]
struct Game {
    id: usize,
    red: usize,
    green: usize,
    blue: usize,
}

impl Game {
    fn power(&self) -> usize {
        self.red * self.green * self.blue
    }
}

// Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
// Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
// Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
// Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
// Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

fn parse_game(inp: &'static str) -> Game {
    let inp = skip_word(inp);
    let (id, inp) = parse_num(inp);
    let inp = skip_word(inp);
    let mut game = Game { id, red: 0, green: 0, blue: 0 };

    for s in inp.split(';') {
        for cubes in s.split(',') {
            let (n, cubes) = parse_num(cubes);
            if cubes.starts_with("red") { game.red = game.red.max(n); }
            else if cubes.starts_with("blue") { game.blue = game.blue.max(n); }
            else if cubes.starts_with("green") { game.green = game.green.max(n); }
            else {
                dbg!(cubes);
                unreachable!();
            }
        }
    }

    // dbg!(game);
    game
}

// fn max_cubes(a: &Game, b: &Game) -> usize {
//     Game {red: a.red.max(b.red),  green: a.green.max(b.green), blue: a.blue.max(b.blue)}
// }

fn possible(a: &Game) -> bool {
    a.red <= 12 && a.green <= 13 && a.blue <= 14
}

fn parse(_input: &'static str) -> Vec<Game> {
    _input.lines()
        .map(|s| parse_game(s))
        .collect()
}

//------------------------------ SOLVE


fn solve(_input: &'static str, _part: usize) -> usize {
    if _part == 1 {
        parse(_input)
            .iter()
            .filter(|g| possible(g))
            .map(|g| g.id)
            .sum()
    } else {
        parse(_input)
            .iter()
            .map(|g| g.power())
            .sum()
    }
}

//------------------------------ PART 1

#[aoc(day2, part1)]
fn day2_part1(_input: &'static str) -> usize {
    let ans = solve(_input, 1);
    assert_eq!(ans, 2149);
    ans

}

#[test]
fn test_day2_part1() {
    assert_eq!(solve(_SAMPLE, 1), _ANS1);
}

//------------------------------ PART 2

#[aoc(day2, part2)]
fn day2_part2(_input: &'static str) -> usize {
    let ans = solve(_input, 2);
    assert_eq!(ans, 71274);
    ans
}

#[test]
fn test_day2_part2() {
    assert_eq!(solve(_SAMPLE, 2), _ANS2);
}

//------------------------------ SAMPLE DATA

const _SAMPLE: &str = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green";

const _ANS1: usize = 8;
const _ANS2: usize = 2286;