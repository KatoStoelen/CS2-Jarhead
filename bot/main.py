import json
from pathlib import Path

import sc2

import random
import sc2
from sc2 import Race, Difficulty, run_game
from sc2.constants import *
from sc2.player import Bot, Computer
from sc2.helpers import ControlGroup

class MyBot(sc2.BotAI):
    with open(Path(__file__).parent / "../botinfo.json") as f:
        NAME = json.load(f)["name"]

    def __init__(self):
        self.attack_groups = set()

    async def on_step(self, iteration):
        if iteration == 0:
            await self.chat_send(f"Name: {self.NAME}")
        self.iteration = iteration
        if self.units(COMMANDCENTER).exists:
            self.cc = self.units(COMMANDCENTER).first

        await self.commandcenter_is_missing()
        await self.group_idle_marines()
        await self.train_scv()
        await self.build_supplydepot()
        await self.build_barracks()
        await self.train_marines()
        await self.collect_with_scv()
        await self.attack_with_marines()

    async def train_scv(self):
        #train SCVs
        if self.can_afford(SCV) and self.workers.amount < 16 and self.cc.noqueue:
            await self.do(self.cc.train(SCV))

    async def build_barracks(self):
        #build barracks
        if self.units(BARRACKS).amount < 3 or (self.minerals > 400 and self.units(BARRACKS).amount < 5):
            if self.can_afford(BARRACKS):
                p = self.game_info.map_center.towards(self.enemy_start_locations[0], 25)
                await self.build(BARRACKS, near=p)

    async def build_supplydepot(self):
        #build supply depot
        if self.supply_left < (2 if self.units(BARRACKS).amount < 3 else 4):
            if self.can_afford(SUPPLYDEPOT) and self.already_pending(SUPPLYDEPOT) < 2:
                await self.build(SUPPLYDEPOT, near=self.cc.position.towards(self.game_info.map_center, 5))

    async def train_marines(self):
        #train marines
        for rax in self.units(BARRACKS).ready.noqueue:
            if not self.can_afford(MARINE):
                break
            await self.do(rax.train(MARINE))

    async def collect_with_scv(self):
        #collect with SCV
        for scv in self.units(SCV).idle:
            await self.do(scv.gather(self.state.mineral_field.closest_to(self.cc)))

    async def attack_with_marines(self):
        #attack with marines
        for ac in list(self.attack_groups):
            alive_units = ac.select_units(self.units)
            if alive_units.exists and alive_units.idle.exists:
                target = self.known_enemy_structures.random_or(self.enemy_start_locations[0]).position
                for marine in ac.select_units(self.units):
                    await self.do(marine.attack(target))
            else:
                self.attack_groups.remove(ac)

    async def commandcenter_is_missing(self):
        #if command center is missing, all out attack
        if not self.units(COMMANDCENTER).exists:
            target = self.known_enemy_structures.random_or(self.enemy_start_locations[0]).position
            for unit in self.workers | self.units(MARINE):
                await self.do(unit.attack(target))

    async def group_idle_marines(self):
        #group the marines, so they attack together
        if self.units(MARINE).idle.amount > 15 and self.iteration % 50 == 1:
            cg = ControlGroup(self.units(MARINE).idle)
            self.attack_groups.add(cg)


