from dataclasses import dataclass
import yaml
from typing import Optional
import logging
import os


logger = logging.getLogger(__name__)

@dataclass
class TgBot:
    threshold: float
    admin_id: int
    token: str
    url: str




def load_config(path: Optional[str]) -> TgBot:

    if path is None:
        logger.error('Не указан путь для конфига бота')
        raise ValueError

    with open(path, 'r') as f:
            data = yaml.safe_load(f)

    return TgBot(**data['bot'], token=os.environ['BOT_TOKEN'], 
                 url=os.environ['API_URL'])

