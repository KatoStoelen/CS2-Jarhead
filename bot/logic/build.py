import random
import sc2
from sc2.ids.unit_typeid import UnitTypeId


class Builder:
    async def on_step(self, bot: sc2.BotAI):
        await self.build_supplydepot(bot)
        await self.build_barracks(bot)

    async def build_supplydepot(self, bot: sc2.BotAI):
        # build supply depot
        if bot.supply_left < (2 if bot.units(UnitTypeId.BARRACKS).amount < 3 else 4):
            if bot.can_afford(UnitTypeId.SUPPLYDEPOT) and bot.already_pending(UnitTypeId.SUPPLYDEPOT) < 2:
                await bot.build(UnitTypeId.SUPPLYDEPOT, near=bot.cc.position.towards(bot.game_info.map_center, 5))

    async def build_barracks(self, bot: sc2.BotAI):
        # build barracks
        if bot.units(UnitTypeId.BARRACKS).amount < 3 or (bot.minerals > 400 and bot.units(UnitTypeId.BARRACKS).amount < 5):
            if bot.can_afford(UnitTypeId.BARRACKS):
                p = bot.game_info.map_center.towards(
                    bot.enemy_start_locations[0], 25)
                await bot.build(UnitTypeId.BARRACKS, near=p)
