
import torch

from prompts.system_prompt import MERGE_SYSTEM_PROMPT
from llm.load_model import load_model


class OpenChatModel:
    def __init__(self):
        self.model, self.tokenizer = load_model()

    def summarize_text(self, text):
        conversation = [{'role':'system','content':MERGE_SYSTEM_PROMPT},
                    {'role': 'user', 'content': text}]  

        prompt = self.tokenizer.apply_chat_template(conversation, tokenize=False, add_generation_prompt=True)

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device) 

        outputs = self.model.generate(**inputs, 
                                max_new_tokens=4096,
                                top_p=0.3,
                                temperature=0.2, 
                                do_sample=True)

        summarized_text = self.tokenizer.decode(outputs[0],skip_special_tokens=True) 
        summarized_text = self.cut_off_text(summarized_text, '</s>')
        summarized_text = self.remove_substring(summarized_text, prompt)

        return summarized_text

    def cut_off_text(self, text, prompt):
        cutoff_phrase = prompt
        index = text.find(cutoff_phrase)
        if index != -1:
            return text[:index]
        else:
            return text

    def remove_substring(self, string, substring):
        return string.replace(substring, "")
