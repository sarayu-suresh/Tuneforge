# backend/inference.py
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def generate_response(prompt, model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)

    input_text = f"### Instruction:\n{prompt}\n\n### Response:\n"
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=100, temperature=0.7)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("### Response:")[-1].strip()
