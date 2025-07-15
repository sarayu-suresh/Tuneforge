# backend/train.py
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import get_peft_model, LoraConfig, TaskType
import os
import json
import pandas as pd

from transformers import TrainerCallback

class ProgressCallback(TrainerCallback):
    def on_train_begin(self, args, state, control, **kwargs):
        training_status["status"] = "running"
        training_status["total_steps"] = state.max_steps
        training_status["message"] = "Training started"

    def on_step_end(self, args, state, control, **kwargs):
        training_status["current_step"] = state.global_step
        training_status["epoch"] = state.epoch
        training_status["message"] = f"Step {state.global_step}/{state.max_steps}"

    def on_train_end(self, args, state, control, **kwargs):
        training_status["status"] = "done"
        training_status["message"] = "Training complete"

training_status = {
    "status": "idle",         # idle | running | done
    "current_step": 0,
    "total_steps": 0,
    "epoch": 0,
    "message": ""
}


def load_custom_dataset(path):
    if path.endswith('.csv'):
        df = pd.read_csv(path)
    elif path.endswith('.jsonl'):
        df = pd.read_json(path, lines=True)
    else:
        raise ValueError("Unsupported file format")
    return Dataset.from_pandas(df)

def preprocess(example, tokenizer):
    input_text = f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['response']}"
    tokens = tokenizer(input_text, truncation=True, padding="max_length", max_length=512)
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

def fine_tune_model(dataset_path, base_model_name, output_dir):
    dataset = load_custom_dataset(dataset_path)
    tokenizer = AutoTokenizer.from_pretrained(base_model_name)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    tokenized = dataset.map(lambda x: preprocess(x, tokenizer))

    model = AutoModelForCausalLM.from_pretrained(base_model_name)
    config = LoraConfig(task_type=TaskType.CAUSAL_LM, r=8, lora_alpha=32, lora_dropout=0.1, bias="none")
    model = get_peft_model(model, config)

    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=2,
        num_train_epochs=3,
        save_steps=10,
        logging_steps=5,
        save_total_limit=1,
        report_to="none"
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized,
        callbacks=[ProgressCallback()]
    )

    trainer.train()
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
