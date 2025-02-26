import logging

from project.bot import bot


logger = logging.getLogger(__name__)


@bot.listen()
async def on_ready():
    print("запуск")
    logger.info("Бот запущен")
