import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv
import os


from optimization.bnb_config import create_bnb_config
import os
os.environ['TRANSFORMERS_CACHE'] = 'D:/cache'



MODEL_NAME = "openchat/openchat-3.5-0106"


def load_model():
    print('LLAMA2 DOWNLOADING')
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        load_in_4bit=True,
        torch_dtype=torch.float16,
        device_map="auto", 
    )
    print('Модель скачалась')
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    tokenizer.pad_token = tokenizer.eos_token
    print('Токенизатор скачался')

    return model, tokenizer


# bnb_config = create_bnb_config()
# model, tokenizer = load_model(model_name)


# _ = tokenizer.save_pretrained('models/tokenizer')
# _ = model.save_pretrained('models/model')
