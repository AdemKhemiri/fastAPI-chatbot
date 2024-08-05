import os
import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import bitsandbytes
import torch
from transformers import pipeline
import textwrap

os.environ ['HF_HUB_ENABLE_HF_TRANSFER'] = '1'

torch.set_default_device('cuda')


class LLMModel:
    def __init__(self):
        pass
    def initialize_LLM(self, llm_name="mistralai/Mistral-7B-Instruct-v0.3"):

        # use the commented out parts for running in 4bit
        quantization_config = BitsAndBytesConfig(load_in_4bit=True)

        model = AutoModelForCausalLM.from_pretrained(llm_name,
                                                    quantization_config=quantization_config,
                                                    #  low_cpu_mem_usage=True,
                                                    #  torch_dtype="auto",
                                                    torch_dtype=torch.bfloat16,
                                                    device_map="auto")

        tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")

        generation_config = model.generation_config
        generation_config.max_new_tokens = 200
        generation_config.temperature = 0.0
        # generation_config.top_p = 0.7
        # generation_config.num_return_sequences = 1
        generation_config.pad_token_id = tokenizer.eos_token_id
        generation_config.eos_token_id = tokenizer.eos_token_id
        generation_config

        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            model_kwargs={"torch_dtype": torch.bfloat16},
            # device="cuda",
        )
        return pipe


    def wrap_text(self, text, width=90): #preserve_newlines
        # Split the input text into lines based on newline characters
        lines = text.split('\n')
        # Wrap each line individually
        wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
        # Join the wrapped lines back together using newline characters
        wrapped_text = '\n'.join(wrapped_lines)
        return wrapped_text

    async def generate(self, input_text, system_prompt="",max_length=512, pipe=None):
        if system_prompt != "":
            system_prompt = system_prompt
        else:
            system_prompt = "You are a friendly and helpful assistant"
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            # {"role": "user", "content": system_prompt +'\n\n' + input_text},
            {"role": "user", "content": '\n\n' + input_text},
        ]

        prompt = pipe.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
                )
        terminators = [
            pipe.tokenizer.eos_token_id,
            pipe.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]

        outputs = pipe(
            prompt,
            max_new_tokens=max_length,
            eos_token_id=terminators,
            pad_token_id=pipe.tokenizer.eos_token_id,
            do_sample=False,
            # temperature=0.0,
            # top_p=0.9,
        )

        generated_outputs = outputs[0]["generated_text"]
        text = outputs[0]["generated_text"][len(prompt):]
        wrapped_text = self.wrap_text(text)
        return wrapped_text
