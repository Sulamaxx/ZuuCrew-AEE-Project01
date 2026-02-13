"""
Synthetic Dataset Generation for Project 01
"""

import sys
import os
import json
import random
from tqdm import tqdm
from typing import List, Dict

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.services.llm_services import load_config, get_llm
from src.utils.data_processing import load_and_clean_pdf, chunk_text
from src.utils.json_helper import extract_json_from_llm

# System prompts based on assessment constraints
QUESTION_GEN_SYSTEM = """You are a financial analyst. Based on the provided chunk from Uber's 2024 Annual Report, generate 10 distinct questions.
Return ONLY a JSON list of strings. No preamble."""

ANSWER_GEN_SYSTEM = """You are a financial analyst. Answer the following questions based strictly on the provided context.
Return ONLY a JSON list of objects: [{"question": "...", "answer": "..."}]."""

def generate_dataset():
    # Adjusted for running from src/scripts
    config_path = os.path.join(os.path.dirname(__file__), '../config/config.yaml')
    config = load_config(config_path)
    llm = get_llm(config)
    
    # Resolve absolute path to the data
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    pdf_path = config['pdf_path'].lstrip('./')
    pdf_abs_path = os.path.join(project_root, pdf_path)
    
    text = load_and_clean_pdf(pdf_abs_path)
    chunks = chunk_text(text, config['chunk_size'], config['chunk_overlap'])
    
    dataset = []
    target_chunks = chunks[:20] 
    
    for i, chunk in enumerate(tqdm(target_chunks, desc="Generating Q/A pairs")):
        try:
            # Step A: Question Generation
            q_response = llm.invoke([
                ("system", QUESTION_GEN_SYSTEM),
                ("user", f"Context: {chunk}")
            ])
            questions = extract_json_from_llm(q_response.content)
            if not questions:
                print(f"Failed to parse questions for chunk {i}")
                continue
            
            # Step B: Answer Generation
            a_response = llm.invoke([
                ("system", ANSWER_GEN_SYSTEM),
                ("user", f"Context: {chunk}\n\nQuestions: {json.dumps(questions)}")
            ])
            pairs = extract_json_from_llm(a_response.content)
            if not pairs:
                print(f"Failed to parse answers for chunk {i}")
                continue
            
            dataset.extend(pairs)
        except Exception as e:
            print(f"Error in chunk {i}: {e}")
            continue

    # Split 80/20
    random.shuffle(dataset)
    split_idx = int(0.8 * len(dataset))
    train_set = dataset[:split_idx]
    test_set = dataset[split_idx:]
    
    output_dir = os.path.join(project_root, config['train_data_path'].lstrip('./'))
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/train.jsonl", 'w', encoding='utf-8') as f:
        for item in train_set:
            f.write(json.dumps(item) + "\n")
            
    with open(f"{output_dir}/golden_test_set.jsonl", 'w', encoding='utf-8') as f:
        for item in test_set:
            f.write(json.dumps(item) + "\n")

    print(f"Saved {len(train_set)} training pairs and {len(test_set)} test pairs.")

if __name__ == "__main__":
    generate_dataset()
