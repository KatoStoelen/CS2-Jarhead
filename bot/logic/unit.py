import random
import sc2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.helpers import ControlGroup


class UnitController:
    def __init__(self):
        self.attack_groups = set()

    async def on_step(self, bot: sc2.BotAI, iteration: int):
        await self.__group_idle_units(bot)
        await self.__attack(bot)
        await self.__collect_with_scv(bot)

    async def __collect_with_scv(self, bot: sc2.BotAI):
        # collect with SCV
        for scv in bot.units(UnitTypeId.SCV).idle:
            await bot.do(scv.gather(bot.state.mineral_field.closest_to(bot.cc)))
        
        for a in bot.units(UnitTypeId.REFINERY):
            if a.assigned_harvesters < a.ideal_harvesters:
                w = bot.workers.closer_than(20, a)
                if w.exists:
                    await bot.do(w.random.gather(a))

    async def __group_idle_units(self, bot: sc2.BotAI):
        if bot.time > 480:
            idle_units = bot.units(UnitTypeId.MARINE).idle | bot.units(UnitTypeId.REAPER).idle

            if not bot.cc:
                idle_units = idle_units | bot.workers

            if idle_units.amount > 20:
                self.attack_groups.add(ControlGroup(idle_units))

    async def __attack(self, bot: sc2.BotAI):
        for ac in list(self.attack_groups):
            alive_units = ac.select_units(bot.units)
            if alive_units.exists and alive_units.idle.exists:
                target = bot.known_enemy_structures.random_or(
                    bot.enemy_start_locations[0]).position
                for marine in ac.select_units(bot.units):
                    await bot.do(marine.attack(target))
            else:
                self.attack_groups.remove(ac)


