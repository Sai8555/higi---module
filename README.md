# higi 🛡️

[![Test Workflow](https://github.com/sai8555/higi---module/actions/workflows/test.yml/badge.svg)](https://github.com/sai8555/higi---module/actions)
[![PyPI version](https://img.shields.io/pypi/v/higi.svg)](https://pypi.org/project/higi/)
[![Python Versions](https://img.shields.io/pypi/pyversions/higi.svg)](https://pypi.org/project/higi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The universal runtime resilience and self-healing engine for modern Python applications.

## 🛑 The Problem

In the era of AI agents, LLMs, and real-time data streams, software execution has become unpredictable. Traditional validation libraries like Pydantic or JSONSchema are great for catching structural errors, but **they are designed to crash your application when an error is found.**

If an LLM drops tokens and returns a truncated JSON string, or if an API accidentally passes an integer as a string, your production loop breaks. Writing endless defensive `try/except` blocks makes code messy, unmaintainable, and bloated.

## ✨ The Solution: `higi` doesn't crash—it heals.

`higi` acts as a fault-tolerant structural middleware layer. It sits directly between volatile, dynamic inputs (like AI outputs or unpredictable webhooks) and your strict core application logic. 

* **Auto-Healing Parser:** Automatically reconstructs fragmented or unclosed JSON structures on the fly using a stack-based (LIFO) parser.
* **Type Coercion:** Dynamically casts mismatched variables into blueprint compliance (e.g., converting `"200"` to `200` or `"yes"` to `True`).
* **Zero-Crash Fail-Safes:** Gracefully falls back to a shadow context instead of throwing errors and causing system downtime.

---

## ⚙️ Installation

Install `higi` instantly from PyPI using pip:

```bash
pip install higi
```

---

## 🚀 Quick Start & Usage

Protecting your critical execution pipelines is as simple as adding a single python decorator: `@shield`.

```python
from higi import shield

# 1. Define the exact structural blueprint your code expects
blueprint = {
    "status_code": int,
    "message": str,
    "is_active": bool,
    "score": float
}

# 2. Define a clean fallback state if data is completely unrecoverable
fallback = {
    "status_code": 500,
    "message": "HIGI_AUTO_HEAL_FALLBACK",
    "is_active": False,
    "score": 0.0
}

# 3. Protect your core function with the shield decorator
@shield(blueprint=blueprint, fallback=fallback)
def process_incoming_stream(clean_data):
    # This core logic is 100% safe. It is guaranteed to never receive malformed data.
    print(f"Processed: {clean_data}")

# ==========================================
# SIMULATION 1: Handling Malformed / Truncated LLM Outputs
# ==========================================

# Missing closing quotes, keys/values with single quotes, and unclosed brackets/braces!
broken_llm_string = "{'status_code': '200', 'message': 'Operational stream fragment, 'is_active': True, 'score': '75.2"

# higi heals it, type-coerces variables, and executes smoothly without a crash!
process_incoming_stream(broken_llm_string)
# Output: Processed: {'status_code': 200, 'message': 'Operational stream fragment', 'is_active': True, 'score': 75.2}

# ==========================================
# SIMULATION 2: Handling Catastrophic Failures
# ==========================================

# Completely unparseable garbage input
garbage_input = "Invalid Payload Network Error Data Drop!!!"

# higi seamlessly catches the failure and routes to your fallback dictionary instead of crashing
process_incoming_stream(garbage_input)
# Output: Processed: {'status_code': 500, 'message': 'HIGI_AUTO_HEAL_FALLBACK', 'is_active': False, 'score': 0.0}
```

---

## 🛠️ Core Blueprint Engine Architecture

When an input enters a function wrapped by `higi`, it passes through a 3-stage validation and correction pipeline:

1. **Structural Sanitization:** If the input is a raw string, `higi` evaluates the string boundaries and repairs broken structures (such as unclosed braces `{}` or brackets `[]`) using a LIFO stack-based approach. It also normalizes single quotes to double quotes, and capital Python booleans/None to JSON true/false/null.
2. **Type Enforcement & Coercion:** It maps the repaired data against your targeted configuration blueprint, automatically converting loose input types into matching Python primitives (e.g., string integers to `int`, float representation to `float`, and truthy/falsy strings/numbers to `bool`).
3. **Graceful Routing:** If structural anomalies are fully corrupted beyond repair, it automatically substitutes the input parameters with the preset fallback rules.

---

## 🧪 Testing

To run the unit test suite locally:

```bash
PYTHONPATH=. pytest tests/
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👥 Contributing

Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make to expand `higi`'s resilience capabilities are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

Created with 🧠 by [JANAPAREDDY GIRI SAI DURGA](https://github.com/sai8555)
