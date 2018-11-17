import sc2
import random
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2


class Builder:
    async def on_step(self, bot: sc2.BotAI, iteration: int):
        await self.__build_supplydepot(bot)
        await self.__build_refinery(bot)
        await self.__build_barracks(bot)

    async def __build_supplydepot(self, bot: sc2.BotAI):
        # build supply depot
        if bot.supply_left < (2 if bot.units(UnitTypeId.BARRACKS).amount < 3 else 4):
            if bot.can_afford(UnitTypeId.SUPPLYDEPOT) and bot.already_pending(UnitTypeId.SUPPLYDEPOT) < 2:
                await bot.build(UnitTypeId.SUPPLYDEPOT, near=bot.cc.position.random_on_distance(5))

    async def __build_barracks(self, bot: sc2.BotAI):
        if bot.units(UnitTypeId.BARRACKS).amount < 5:
            if bot.can_afford(UnitTypeId.BARRACKS):
                await bot.build(UnitTypeId.BARRACKS, near=bot.main_base_ramp.top_center.towards(bot.cc, 8).random_on_distance(3))

    async def __build_refinery(self, bot: sc2.BotAI):
        if bot.units(UnitTypeId.REFINERY).amount < 2:
                if bot.can_afford(UnitTypeId.REFINERY):
                    vgs = bot.state.vespene_geyser.closer_than(20.0, bot.cc)
                    for vg in vgs:
                        if bot.units(UnitTypeId.REFINERY).closer_than(1.0, vg).exists:
                            break

                        worker = bot.select_build_worker(vg.position)
                        if worker is None:
                            break

                        await bot.do(worker.build(UnitTypeId.REFINERY, vg))
                        break
