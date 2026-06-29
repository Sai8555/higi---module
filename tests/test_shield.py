import pytest
from higi.shield import shield, HigisEngine

def test_heal_input_string_valid():
    engine = HigisEngine({})
    assert engine.heal_input_string('{"a": 1}') == '{"a": 1}'
    assert engine.heal_input_string('[1, 2, 3]') == '[1, 2, 3]'

def test_heal_input_string_single_quotes():
    engine = HigisEngine({})
    # Single quotes around keys/values
    assert engine.heal_input_string("{'a': 1, 'b': 'hello'}") == '{"a": 1, "b": "hello"}'
    # Single quotes with escaped single quote
    assert engine.heal_input_string("{'name': 'John \\'Doe\\''}") == '{"name": "John \\\'Doe\\\'"}'

def test_heal_input_string_python_literals():
    engine = HigisEngine({})
    assert engine.heal_input_string("{'flag': True, 'none': None}") == '{"flag": true, "none": null}'

def test_heal_input_string_truncation():
    engine = HigisEngine({})
    # Unclosed brace
    assert engine.heal_input_string('{"name": "John"') == '{"name": "John"}'
    assert engine.heal_input_string('{"name": "John') == '{"name": "John"}'
    assert engine.heal_input_string('{"items": [1, 2') == '{"items": [1, 2]}'
    assert engine.heal_input_string('{"items": [{"name": "item1"}, {"name": "item2') == '{"items": [{"name": "item1"}, {"name": "item2"}]}'

def test_enforce_blueprint():
    blueprint = {
        "name": str,
        "age": int,
        "is_active": bool,
        "score": float,
        "tags": list,
        "meta": dict
    }
    fallback = {
        "name": "Unknown",
        "age": 0,
        "is_active": False,
        "score": 0.0,
        "tags": [],
        "meta": {}
    }
    engine = HigisEngine(blueprint)
    
    # 1. Exact matches
    data = {
        "name": "Alice",
        "age": 25,
        "is_active": True,
        "score": 95.5,
        "tags": ["a", "b"],
        "meta": {"ip": "127.0.0.1"}
    }
    assert engine.enforce_blueprint(data, fallback) == data
    
    # 2. Type coercion
    input_data = {
        "name": 123,           # should become "123"
        "age": "30",          # should become 30
        "is_active": "yes",   # should become True
        "score": 100,         # should become 100.0
        "tags": "not_a_list", # should fallback
        "meta": "not_a_dict"  # should fallback
    }
    expected = {
        "name": "123",
        "age": 30,
        "is_active": True,
        "score": 100.0,
        "tags": [],
        "meta": {}
    }
    assert engine.enforce_blueprint(input_data, fallback) == expected

def test_shield_decorator():
    blueprint = {"id": int, "username": str}
    fallback = {"id": -1, "username": "guest"}
    
    @shield(blueprint, fallback)
    def process_user(user_data):
        return user_data

    # Valid dict
    assert process_user({"id": 42, "username": "john"}) == {"id": 42, "username": "john"}
    
    # Valid JSON string
    assert process_user('{"id": 42, "username": "john"}') == {"id": 42, "username": "john"}
    
    # Malformed JSON string (single quotes, trailing comma, unclosed)
    assert process_user("{'id': '42', 'username': 'john',") == {"id": 42, "username": "john"}
    
    # Fully corrupted string (should trigger fallback)
    assert process_user("invalid json entirely") == fallback
