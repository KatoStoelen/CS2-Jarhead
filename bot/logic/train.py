import sc2
from sc2.ids.unit_typeid import UnitTypeId


class Trainer:
    async def on_step(self, bot: sc2.BotAI, iteration: int):
        await self.__train_scv(bot)
        await self.__train_siegetank(bot)
        await self.__train_marines(bot)
        await self.__train_reapers(bot)

    async def __train_scv(self, bot: sc2.BotAI):
        # train SCVs
        if bot.can_afford(UnitTypeId.SCV) and bot.workers.amount < 20 and bot.cc.noqueue:
            await bot.do(bot.cc.train(UnitTypeId.SCV))

    async def __train_marines(self, bot: sc2.BotAI):
        # train marines
        if bot.units(UnitTypeId.MARINE).amount < 10 or bot.units(UnitTypeId.MARINE).amount < bot.units(UnitTypeId.REAPER).amount*5:
            for rax in bot.units(UnitTypeId.BARRACKS).ready.noqueue:
                if not bot.can_afford(UnitTypeId.MARINE):
                    break
                await bot.do(rax.train(UnitTypeId.MARINE))
            
    async def __train_siegetank(self, bot: sc2.BotAI):
        for fact in bot.units(UnitTypeId.FACTORY).ready.noqueue:
            if not bot.can_afford(UnitTypeId.SIEGETANK):
                break
            await bot.do(fact.train(UnitTypeId.SIEGETANK))
    
    async def __train_reapers(self, bot: sc2.BotAI):
        for rax in bot.units(UnitTypeId.BARRACKS).ready.noqueue:
            if not bot.can_afford(UnitTypeId.REAPER):
                break
            await bot.do(rax.train(UnitTypeId.REAPER))




