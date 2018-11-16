import sc2
from sc2.ids.unit_typeid import UnitTypeId
from .logic import Builder, Trainer, UnitController, Chatter


class MyBot(sc2.BotAI):
    def __init__(self):
        self.builder = Builder()
        self.trainer = Trainer()
        self.unitController = UnitController()
        self.chatter = Chatter()

    async def on_step(self, iteration):
        self.iteration = iteration
        if self.units(UnitTypeId.COMMANDCENTER).exists:
            self.cc = self.units(UnitTypeId.COMMANDCENTER).first

        await self.unitController.on_step(self, iteration)
        await self.trainer.on_step(self, iteration)
        await self.builder.on_step(self, iteration)
        await self.chatter.on_step(self, iteration)
