import sc2
from sc2.ids.unit_typeid import UnitTypeId
from .logic import Builder, Trainer, UnitController


class MyBot(sc2.BotAI):
    def __init__(self):
        self.builder = Builder()
        self.trainer = Trainer()
        self.unitController = UnitController()

    async def on_step(self, iteration):
        self.iteration = iteration
        if self.units(UnitTypeId.COMMANDCENTER).exists:
            self.cc = self.units(UnitTypeId.COMMANDCENTER).first

        await self.unitController.on_step(self)
        await self.trainer.on_step(self)
        await self.builder.on_step(self)
