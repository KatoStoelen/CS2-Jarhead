import sc2
from sc2.ids.unit_typeid import UnitTypeId


class Builder:
    async def on_step(self, bot: sc2.BotAI, iteration: int):
        await self.__build_supplydepot(bot)
        await self.__build_base_barracks(bot)
        await self.__build_chokepoint_bunker(bot)
        await self.__build_engineering_bay(bot)
        await self.__build_barracks(bot)

    async def __build_supplydepot(self, bot: sc2.BotAI):
        # build supply depot
        if bot.time > 240:
            if bot.supply_left < (2 if bot.units(UnitTypeId.BARRACKS).amount < 3 else 4):
                if bot.can_afford(UnitTypeId.SUPPLYDEPOT) and bot.already_pending(UnitTypeId.SUPPLYDEPOT) < 2:
                    await bot.build(UnitTypeId.SUPPLYDEPOT, near=bot.cc.position.towards(bot.game_info.map_center, 5))

    async def __build_barracks(self, bot: sc2.BotAI):
        # build barracks
        if bot.units(UnitTypeId.BARRACKS).amount < 3 or (bot.minerals > 400 and bot.units(UnitTypeId.BARRACKS).amount < 5):
            if bot.can_afford(UnitTypeId.BARRACKS):
                p = bot.game_info.map_center.towards(
                    bot.enemy_start_locations[0], 25)
                await bot.build(UnitTypeId.BARRACKS, near=p)

    async def __build_chokepoint_bunker(self, bot: sc2.BotAI):
        # build bunker at base choke point
        if bot.units(UnitTypeId.BUNKER).closer_than(10, bot.main_base_ramp.top_center).amount < 2:
            if bot.can_afford(UnitTypeId.BUNKER) and bot.already_pending(UnitTypeId.BUNKER) < 2:
                await bot.build(UnitTypeId.BUNKER, near=bot.main_base_ramp.top_center)

    async def __build_base_barracks(self, bot: sc2.BotAI):
        if bot.units(UnitTypeId.BARRACKS).closer_than(10, bot.main_base_ramp.top_center).amount == 0:
            if bot.can_afford(UnitTypeId.BARRACKS) and bot.already_pending(UnitTypeId.BARRACKS) == 0:
                await bot.build(UnitTypeId.BARRACKS, bot.main_base_ramp.top_center.towards(bot.cc.position, 10))

    async def __build_engineering_bay(self, bot: sc2.BotAI):
        if bot.units(UnitTypeId.ENGINEERINGBAY).amount == 0:
            if bot.can_afford(UnitTypeId.ENGINEERINGBAY) and bot.already_pending(UnitTypeId.ENGINEERINGBAY) == 0:
                await bot.build(UnitTypeId.ENGINEERINGBAY, bot.cc.position.towards(bot.game_info.map_center, 5))

    # async def __build_chokepoint_missile_turret(self, bot: sc2.BotAI):
    #     if bot.units(UnitTypeId.MISSILETURRET).closer_than(5, bot.main_base_ramp.top_center).amount == 0:

