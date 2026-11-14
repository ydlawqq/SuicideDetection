import asyncio, logging, os
from pathlib import Path

from aiogram import Dispatcher, Bot, F, Router
from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError

from bot.client import Client
from bot.config import TgBot, load_config

from aiogram.client.telegram import TelegramAPIServer
from aiogram.client.session.aiohttp import AiohttpSession

from shared.setup_logger import setup_logger

from andro_cfw import CFWSession



router = Router(name='group_mess')


CONFIG_PATH = Path(__file__).parent / "config.yaml"

@router.message(F.chat.type.in_({'group', 'supergroup'}), F.text)
async def on_group_message(message: Message, bot: Bot, client: Client, config: TgBot):
    texts = [message.text]
    username = message.from_user.username
    date = str(message.date)
    score = await client.predict(texts)
    if score[0] > config.threshold:
        await bot.send_message(
            chat_id=config.admin_id,
            text=f'Внимание! У пользователя {username} обнаружен суицидальный сигнал.'
            f'Время сообщения: {date}, Текст: {texts}'
        )



async def main():
    session = CFWSession.load()
    api_server = TelegramAPIServer(**session.aiogram_server_url())
    setup_logger()
    cfg = load_config(CONFIG_PATH)
    client = Client(cfg.url)
    bot = Bot(token=cfg.token, session=AiohttpSession(api=api_server))
    dp = Dispatcher()
    dp['config'] = cfg
    dp['client'] = client
    dp.include_router(router=router)
    try:
        await dp.start_polling(bot)
    finally:
        await client.aclose()


if __name__ == '__main__':
    asyncio.run(main())