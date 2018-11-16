import random
import sc2
from sc2.ids.unit_typeid import UnitTypeId


class Trainer:
    async def on_step(self, bot: sc2.BotAI):
        await self.train_scv(bot)
        await self.train_marines(bot)

    async def train_scv(self, bot: sc2.BotAI):
        # train SCVs
        if bot.can_afford(UnitTypeId.SCV) and bot.workers.amount < 16 and bot.cc.noqueue:
            await bot.do(bot.cc.train(UnitTypeId.SCV))

    async def train_marines(self, bot: sc2.BotAI):
        # train marines
        for rax in bot.units(UnitTypeId.BARRACKS).ready.noqueue:
            if not bot.can_afford(UnitTypeId.MARINE):
                break
            await bot.do(rax.train(UnitTypeId.MARINE))
