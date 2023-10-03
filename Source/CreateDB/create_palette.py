import json

def create_json_palette(default_path, palette_path):
    """Copy default.json as palette.json"""
    with open(default_path, 'r') as file:
        palette = json.load(file)
    with open(palette_path, 'w') as file:
        json.dump(palette, file, ensure_ascii=False, indent=4)