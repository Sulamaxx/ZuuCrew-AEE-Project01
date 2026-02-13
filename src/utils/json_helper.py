import json
import re

def extract_json_from_llm(text: str):
    """
    Robustly extracts JSON from an LLM response string.
    Works for raw JSON, markdown-wrapped JSON, and JSON with surrounding text.
    Modified to attempt recovery for truncated JSON.
    """
    if not text:
        return None
    
    text = text.strip()
    
    # 1. Try to find JSON block in markdown
    match = re.search(r'```(?:json)?\s*(.*?)```', text, re.DOTALL)
    if match:
        content = match.group(1).strip()
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            text = content # Use the block content for further attempts
            
    # 2. Find start and end brackets
    start_match = re.search(r'[\[\{]', text)
    if not start_match:
        return None
        
    start_idx = start_match.start()
    char = text[start_idx]
    end_char = ']' if char == '[' else '}'
    
    end_idx = text.rfind(end_char)
    
    # If no end bracket found, try to fix it (common truncation)
    if end_idx == -1 or end_idx < start_idx:
        # Very crude fix for truncated lists
        if char == '[':
            # Try to close the last open string if any
            if text.count('"') % 2 != 0:
                text += '"'
            text += ']'
            end_idx = len(text) - 1
        else:
            return None # Objects are harder to fix gracefully

    content = text[start_idx:end_idx+1]
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Try one more time by stripping trailing garbage inside the content
        try:
            # Look for the absolute last bracket of the right type
            last_bracket = content.rfind(end_char)
            if last_bracket != -1:
                return json.loads(content[:last_bracket+1])
        except:
            pass
        return None
