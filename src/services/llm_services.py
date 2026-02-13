"""
LLM and Embedding Factory Functions for Project 01
Adapted from Week 03 lecturer patterns.
"""

import os
from typing import Dict, Any
import yaml
from pathlib import Path

def load_config(config_path: str = "src/config/config.yaml") -> Dict[str, Any]:
    # Try local or absolute path
    path = Path(config_path)
    if not path.exists():
        # Try one level up (if called from src/scripts or notebooks/)
        path = Path("..") / config_path
    
    if not path.exists():
        # Try from project root if running from notebooks
        path = Path("../src/config/config.yaml")
        
    with open(path, "r") as f:
        return yaml.safe_load(f)

def get_llm(config: Dict[str, Any]):
    provider = config["llm_provider"]
    if provider == "gemini":
        model_name = config.get("llm_model")
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=config.get("temperature", 0.2),
            max_tokens=config.get("max_tokens", 1024),
            response_mime_type="application/json"
        )
    
    if provider == "openrouter":
        # ... (Removed or kept as fallback)
        pass
        
    raise ValueError(f"Provider {provider} not implemented for Project 01 Factory")

def get_text_embeddings(config: Dict[str, Any]):
    provider = config["text_emb_provider"]
    if provider == "sbert":
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name=config["text_emb_model"],
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": config.get("normalize_embeddings", True)}
        )
    raise ValueError(f"Embedding provider {provider} not implemented")

def validate_api_keys(config: Dict[str, Any], verbose: bool = True):
    import warnings
    api_keys = {
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
        "WEAVIATE_API_KEY": os.getenv("WEAVIATE_API_KEY"),
    }
    availability = {}
    for key, value in api_keys.items():
        availability[key] = value is not None
        if verbose and not value:
            warnings.warn(f"⚠️  {key} not found in environment")
    return availability

def print_config_summary(config: Dict[str, Any]):
    print("✅ Config loaded:")
    print(f"  LLM: {config['llm_provider']} / {config.get('llm_model')}")
    print(f"  Embeddings: {config['text_emb_provider']} / {config['text_emb_model']}")
    print(f"  Temperature: {config.get('temperature')}")
    print(f"  Artifacts: {config.get('artifacts_root')}")
