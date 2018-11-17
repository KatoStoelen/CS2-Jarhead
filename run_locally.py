import json, time, os

from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer

from bot import MyBot


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def main():
    with open("botinfo.json") as f:
        info = json.load(f)

    race = Race[info["race"]]

    milliseconds = int(round(time.time() * 1000))
    assure_path_exists("results/")
    replay_file = "replays/" + str(milliseconds) + ".SC2Replay"

    run_game(maps.get("Abyssal Reef LE"), [
        Bot(race, MyBot()),
        Computer(Race.Random, Difficulty.Medium)
    ], realtime=False, game_time_limit=(60*20), save_replay_as=replay_file)


if __name__ == '__main__':
    main()
