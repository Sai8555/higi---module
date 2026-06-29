import json
import functools
import re
from typing import Any, Dict, Type, Union

class HigisEngine:
    def __init__(self, blueprint: Dict[str, Type]):
        self.blueprint = blueprint

    def heal_input_string(self, raw_str: str) -> str:
        """Fixes common structural truncation and formatting issues from raw streams or LLMs."""
        cleaned = raw_str.strip()
        if not cleaned:
            return cleaned

        # 1. Convert Python-style single quoted keys/values to double quotes
        # Match 'content' where content does not contain unescaped single quotes
        def replace_single_quotes(match):
            s = match.group(1)
            # Escape double quotes inside
            s_escaped = s.replace('"', '\\"')
            return f'"{s_escaped}"'
        cleaned = re.sub(r"'((?:[^'\\]|\\.)*)'", replace_single_quotes, cleaned)

        # 2. Convert Python-style True, False, None to JSON true, false, null
        cleaned = re.sub(r'\bTrue\b', 'true', cleaned)
        cleaned = re.sub(r'\bFalse\b', 'false', cleaned)
        cleaned = re.sub(r'\bNone\b', 'null', cleaned)

        # 3. Check for unclosed string literal at the end of truncated JSON
        # Count double quotes (excluding escaped ones)
        unescaped_quotes = len(re.findall(r'(?<!\\)"', cleaned))
        if unescaped_quotes % 2 != 0:
            cleaned += '"'

        # 4. LIFO stack-based logic to auto-close unclosed objects and arrays
        stack = []
        in_string = False
        escape = False
        
        for char in cleaned:
            if in_string:
                if escape:
                    escape = False
                elif char == '\\':
                    escape = True
                elif char == '"':
                    in_string = False
            else:
                if char == '"':
                    in_string = True
                elif char in ('{', '['):
                    stack.append(char)
                elif char in ('}', ']'):
                    if stack:
                        top = stack[-1]
                        if (char == '}' and top == '{') or (char == ']' and top == '['):
                            stack.pop()

        if stack:
            cleaned = cleaned.rstrip(', :\n\r\t')
            for op in reversed(stack):
                if op == '{':
                    cleaned += '}'
                elif op == '[':
                    cleaned += ']'

        return cleaned

    def enforce_blueprint(self, data: Dict, fallback: Dict) -> Dict:
        """Ensures the final dictionary perfectly matches expected types with smart coercion."""
        sanitized = {}
        for key, expected_type in self.blueprint.items():
            if key not in data:
                sanitized[key] = fallback.get(key)
                continue
            
            val = data[key]
            
            # If type matches, keep it
            if isinstance(val, expected_type) and not (expected_type is float and isinstance(val, bool)):
                # Note: bool is a subclass of int in Python, so isinstance(True, int) is True.
                # But isinstance(True, float) is False. We should make sure boolean is not coerced improperly.
                sanitized[key] = val
                continue
                
            # Smart data-type coercion
            if expected_type is bool:
                if isinstance(val, str):
                    val_lower = val.strip().lower()
                    if val_lower in ("true", "yes", "1", "t", "y", "on"):
                        sanitized[key] = True
                    elif val_lower in ("false", "no", "0", "f", "n", "off"):
                        sanitized[key] = False
                    else:
                        sanitized[key] = fallback.get(key)
                elif isinstance(val, (int, float)):
                    sanitized[key] = bool(val)
                else:
                    sanitized[key] = fallback.get(key)
                    
            elif expected_type is int:
                try:
                    if isinstance(val, float):
                        sanitized[key] = int(round(val))
                    elif isinstance(val, bool):
                        sanitized[key] = 1 if val else 0
                    else:
                        sanitized[key] = int(val)
                except (ValueError, TypeError):
                    sanitized[key] = fallback.get(key)
                    
            elif expected_type is float:
                try:
                    if isinstance(val, bool):
                        sanitized[key] = 1.0 if val else 0.0
                    else:
                        sanitized[key] = float(val)
                except (ValueError, TypeError):
                    sanitized[key] = fallback.get(key)
                    
            elif expected_type is str:
                if val is None:
                    sanitized[key] = fallback.get(key)
                else:
                    sanitized[key] = str(val)
                    
            elif expected_type in (list, dict):
                if isinstance(val, expected_type):
                    sanitized[key] = val
                else:
                    sanitized[key] = fallback.get(key)
            else:
                # Fallback for complex/custom types
                try:
                    sanitized[key] = expected_type(val)
                except (ValueError, TypeError):
                    sanitized[key] = fallback.get(key)
                    
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
