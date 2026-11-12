from model.model_config import load_config
from pathlib import Path
import torch


CONFIG_PATH = Path(__file__).parent.parent / "config.yaml"



def test_config_load():
    cfg =  load_config(CONFIG_PATH)

    assert isinstance(cfg.model.threshold, float)
    assert isinstance(cfg.model.name, str)
    assert isinstance(cfg.model.labels, int)
    assert isinstance(cfg.model.max_length, int)
    assert cfg.model.path is not None


