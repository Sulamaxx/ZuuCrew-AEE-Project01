import json
import os

notebook_path = r'd:\Zuu Crew\AEE\MY\ZuuCrew-AEE-Project01\notebooks\02_finetuning_intern.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the cell that contains SFTConfig and dataset_text_field
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source_lines = cell['source']
        modified = False
        new_source = []
        for line in source_lines:
            if 'dataset_text_field="text"' in line:
                # Remove the line if it's just this field, or remove the field within the line
                # In the previously viewed content, it was:
                # 336:    "    dataset_text_field=\"text\",\n",
                modified = True
                continue 
            new_source.append(line)
        
        if modified:
            cell['source'] = new_source
            break

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
