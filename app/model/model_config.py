import os
from dataclasses import dataclass
import yaml
import torch
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    name:str
    path: str 
    device: str
    max_length: int
    threshold: float
    dtype: str
    batch_size: int
    labels: int = 1
    

@dataclass
class Config:
    model: ModelConfig




def load_config(path: Optional[str] = None)-> ModelConfig:
    
    if path is None:
        logger.error('Нет путя к конфигу')
        raise ValueError('Не указан путь конфига к модели')

    


    with open(path, 'r') as f:
        data = yaml.safe_load(f)


    return Config(
        model=ModelConfig(**data['model'])
    )