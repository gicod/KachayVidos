import json
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SETTINGS_PATH = ROOT_DIR / "config" / "settings.json"

DEFAULT_SETTINGS = {
    "theme": "dark",
    "download_paths": {
        "youtube": str(Path.home() / "Videos" / "YouTube"),
        "instagram": str(Path.home() / "Videos" / "Instagram"),
    },
    "quality": {
        "youtube": "1080",
        "instagram": "best",
    },
    "container": "mp4",
}

def load_settings():
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not SETTINGS_PATH.exists():
        save_settings(DEFAULT_SETTINGS)
        return json.loads(json.dumps(DEFAULT_SETTINGS))
    try:
        with SETTINGS_PATH.open("r", encoding="utf-8") as file:
            loaded = json.load(file)
    except (OSError, json.JSONDecodeError):
        loaded = {}
    settings = json.loads(json.dumps(DEFAULT_SETTINGS))
    for key, value in loaded.items():
        if isinstance(value, dict) and isinstance(settings.get(key), dict):
            settings[key].update(value)
        else:
            settings[key] = value
    return settings

def save_settings(settings):
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    temp_path = SETTINGS_PATH.with_suffix(".tmp")
    with temp_path.open("w", encoding="utf-8") as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)
    os.replace(temp_path, SETTINGS_PATH)
