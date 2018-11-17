import random
import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.helpers import ControlGroup


class UnitController:
    def __init__(self):
        self.attack_groups = set()

    async def on_step(self, bot: sc2.BotAI, iteration: int):
        await self.__all_out_attack(bot)
        # await self.__group_idle_marines(bot, iteration)
        await self.__collect_with_scv(bot)
        # await self.__attack_with_marines(bot)

    async def __collect_with_scv(self, bot: sc2.BotAI):
        # collect with SCV
        for scv in bot.units(UnitTypeId.SCV).idle:
            await bot.do(scv.gather(bot.state.mineral_field.closest_to(bot.cc)))
        
        for a in bot.units(UnitTypeId.REFINERY):
            if a.assigned_harvesters < a.ideal_harvesters:
                w = bot.workers.closer_than(20, a)
                if w.exists:
                    await bot.do(w.random.gather(a))

    async def __group_idle_marines(self, bot: sc2.BotAI, iteration: int):
        # group the marines, so they attack together
        if bot.units(UnitTypeId.MARINE).idle.amount > 15 and iteration % 50 == 1:
            cg = ControlGroup(bot.units(UnitTypeId.MARINE).idle)
            self.attack_groups.add(cg)

    async def __attack_with_marines(self, bot: sc2.BotAI):
        # attack with marines
        for ac in list(self.attack_groups):
            alive_units = ac.select_units(bot.units)
            if alive_units.exists and alive_units.idle.exists:
                target = bot.known_enemy_structures.random_or(
                    bot.enemy_start_locations[0]).position
                for marine in ac.select_units(bot.units):
                    await bot.do(marine.attack(target))
            else:
                self.attack_groups.remove(ac)

    async def __all_out_attack(self, bot: sc2.BotAI):
        # if command center is missing, all out attack
        if bot.time > 480:
            target = bot.known_enemy_structures.random_or(
                bot.enemy_start_locations[0]).position
            for unit in bot.workers | bot.units(UnitTypeId.MARINE) | bot.units(UnitTypeId.MARAUDER) | bot.units(UnitTypeId.SIEGETANK):
                await bot.do(unit.attack(target))

    async def __worker_defence(self, bot: sc2.BotAI):
        
        target = bot.known_enemy_structures.random_or(bot.enemy_start_locations[0]).position
        for unit in bot.workers:
            await bot.do(unit.attack(target))

