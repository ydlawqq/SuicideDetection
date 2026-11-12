from torch.utils.data import Dataset
import re
import emoji


def prepare(text):         
    clean_tags = re.sub(r'<emoji>\s*(.*?)\s*</emoji>', lambda m: f":{m.group(1).strip().replace(' ', '_').lower()}:", text)
    emojified = emoji.emojize(clean_tags, language='en')
    

    ru_demojized = emoji.demojize(emojified, language='ru')
    

    final_text = ru_demojized.replace('::', ' ').replace(':', ' ').replace('_', ' ')
    final_text = re.sub(r'\s+', ' ', final_text).strip()
    final_text = re.sub(r'[,;:«»""()\[\]{}]', ' ', final_text)

    return final_text




