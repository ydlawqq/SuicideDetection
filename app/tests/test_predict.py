from model.predictor import Model
from model.model_config import load_config
from .test_config import CONFIG_PATH
import pytest
import torch
from  typing import List

cfg = load_config(CONFIG_PATH)


@pytest.mark.parametrize('t', [['Привет, как дела?', 'Что делаешь?'], ['Ты дурак!', 'Отойди от меня', 'Не трогай его!'], ['Отойди от меня пожалуйста']])
def test_model_call(t: List[str]):

    
    m = Model(cfg)
    logits = m.predict(t)
    assert (len(logits) > 0)
    assert len(t) == len(logits)