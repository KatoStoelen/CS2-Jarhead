import sc2


class Chatter:
    async def on_step(self, bot: sc2.BotAI, iteration: int):
        await self.__writeGreeting(bot, iteration)

    async def __writeGreeting(self, bot: sc2.BotAI, iteration: int):
        if iteration == 1:
            await bot.chat_send("GLHF")
        if iteration == 60:
            await bot.chat_send("You SUCK!")
