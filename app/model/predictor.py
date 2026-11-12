from transformers import AutoModelForSequenceClassification, AutoTokenizer
import re
import emoji
import torch
from .utils import prepare
import logging

logger = logging.getLogger(__name__)

class Model:


    def __init__(self, config):
        self.device = torch.device(config.model.device)
        logger.info('Загрузка модели')
        self.model = AutoModelForSequenceClassification.from_pretrained(
            pretrained_model_name_or_path=config.model.name, 
            num_labels=config.model.labels, dtype=getattr(torch, config.model.dtype)
        ).to(self.device)
        state_dict = torch.load(
        config.model.path,
        map_location=config.model.device,
        weights_only=True
        )

        self.model.load_state_dict(state_dict)
        self.tokenizer = AutoTokenizer.from_pretrained(config.model.name)
        self.model.config.pad_token_id = self.tokenizer.pad_token_id
        self.max_length = config.model.max_length
        self.threshold = config.model.threshold
        self.model.eval()
        logger.info('Модель загружена')

    @torch.inference_mode()
    def predict(self, texts):
        

        texts = list(map(prepare, texts))
        texts = self.tokenizer(texts, return_tensors='pt', truncation=True, padding=True, max_length=self.max_length)

        batch = {k: v.to(self.device) for k, v in texts.items()}

        logits = self.model(**batch).logits.squeeze(-1)
        result = torch.sigmoid(logits).tolist()

        return result



        




    