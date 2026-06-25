import json
import functools
from typing import Any, Dict, Type, Union

class HigisEngine:
    def __init__(self, blueprint: Dict[str, Type]):
        self.blueprint = blueprint

    def heal_input_string(self, raw_str: str) -> str:
        """Fixes common structural truncation from raw streams or LLMs."""
        cleaned = raw_str.strip()
        
        # Simple self-healing logic for unclosed JSON objects
        if cleaned.startswith("{") and not cleaned.endswith("}"):
            if cleaned.endswith(",") or cleaned.endswith('"'):
                cleaned = cleaned.rstrip(', "')
            cleaned += "}"
        elif cleaned.startswith("[") and not cleaned.endswith("]"):
            cleaned += "]"
        return cleaned

    def enforce_blueprint(self, data: Dict, fallback: Dict) -> Dict:
        """Ensures the final dictionary perfectly matches expected types."""
        sanitized = {}
        for key, expected_type in self.blueprint.items():
            if key not in data:
                sanitized[key] = fallback.get(key)
                continue
            
            val = data[key]
            # Smart data-type coercion (e.g., casting "123" string into 123 int)
            if not isinstance(val, expected_type):
                try:
                    sanitized[key] = expected_type(val)
                except (ValueError, TypeError):
                    sanitized[key] = fallback.get(key)
            else:
                sanitized[key] = val
        return sanitized

def shield(blueprint: dict, fallback: dict):
    """The protective decorator to stop malformed runtime strings from crashing code."""
    engine = HigisEngine(blueprint)
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(raw_input: Union[str, dict], *args, **kwargs):
            if isinstance(raw_input, str):
                try:
                    healed = engine.heal_input_string(raw_input)
                    parsed_data = json.loads(healed)
                except Exception:
                    return func(fallback, *args, **kwargs)
            else:
                parsed_data = raw_input

            clean_data = engine.enforce_blueprint(parsed_data, fallback)
            return func(clean_data, *args, **kwargs)
        return wrapper
    return decorator
