import sc2
from sc2.ids.unit_typeid import UnitTypeId


class Trainer:
    async def on_step(self, bot: sc2.BotAI, iteration: int):
        await self.__train_scv(bot)
        await self.__train_marines(bot)
        await self.__train_base_marines(bot)
        #await self.__train_marauder(bot)

    async def __train_scv(self, bot: sc2.BotAI):
        # train SCVs
        if bot.can_afford(UnitTypeId.SCV) and bot.workers.amount < 16 and bot.cc.noqueue:
            await bot.do(bot.cc.train(UnitTypeId.SCV))

    async def __train_marines(self, bot: sc2.BotAI):
        # train marines
        for rax in bot.units(UnitTypeId.BARRACKS).closer_than(25, bot.game_info.map_center.towards(bot.enemy_start_locations[0],25)).ready.noqueue:
            if not bot.can_afford(UnitTypeId.MARINE):
                break
            await bot.do(rax.train(UnitTypeId.MARINE))
    
    async def __train_base_marines(self, bot: sc2.BotAI):
        base_bunkers = bot.units(UnitTypeId.BUNKER).closer_than(15, bot.main_base_ramp.top_center)
        for bunker in base_bunkers:
            if bunker.cargo_used < bunker.cargo_max:
                for rax in bot.units(UnitTypeId.BARRACKS).closer_than(15, bot.main_base_ramp.top_center).ready.noqueue:
                    if not bot.can_afford(UnitTypeId.MARINE):
                        return
                    await bot.do(rax.train(UnitTypeId.MARINE))



