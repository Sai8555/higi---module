
# higi 🛡️

The universal runtime resilience and self-healing engine for modern Python applications.

[![PyPI version](https://img.shields.io/pypi/v/higi.svg)](https://pypi.org/project/higi/)
[![Python Versions](https://img.shields.io/pypi/pyversions/higi.svg)](https://pypi.org/project/higi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🛑 The Problem

In the era of AI agents, LLMs, and real-time data streams, software execution has become unpredictable. Traditional validation libraries like Pydantic or JSONSchema are great for catching structural errors, but **they are designed to crash your application when an error is found.**

If an LLM drops tokens and returns a truncated JSON string, or if an API accidentally passes an integer as a string, your production loop breaks. Writing endless defensive `try/except` blocks makes code messy, unmaintainable, and bloated.

## ✨ The Solution: `higi` doesn't crash—it heals.

`higi` acts as a fault-tolerant structural middleware layer. It sits directly between volatile, dynamic inputs (like AI outputs or unpredictable webhooks) and your strict core application logic. 

* **Auto-Healing Parser:** Automatically reconstructs fragmented or unclosed JSON structures on the fly.
* **Type Coercion:** Dynamically casts mismatched variables into blueprint compliance (e.g., converting `"200"` to `200` if an integer is expected).
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
    "message": str
}

# 2. Define a clean fallback state if data is completely unrecoverable
fallback = {
    "status_code": 500,
    "message": "HIGI_AUTO_HEAL_FALLBACK"
}

# 3. Protect your core function with the shield decorator
@shield(blueprint=blueprint, fallback=fallback)
def process_incoming_stream(clean_data):
    # This core logic is 100% safe. It is guaranteed to never receive malformed data.
    print(f"Status Type: {type(clean_data['status_code'])} | Value: {clean_data['status_code']}")
    print(f"Message: {clean_data['message']}")

# ==========================================
# SIMULATION 1: Handling Malformed / Truncated LLM Outputs
# ==========================================

# Missing closing quotes and trailing bracket structures!
broken_llm_string = '{"status_code": "200", "message": "Operational stream fragment'

# higi heals it, type-casts "200" to int, and executes smoothly without a crash!
process_incoming_stream(broken_llm_string)

# ==========================================
# SIMULATION 2: Handling Catastrophic Failures
# ==========================================

# Completely unparseable garbage input
garbage_input = "Invalid Payload Network Error Data Drop!!!"

# higi seamlessly catches the failure and routes to your fallback dictionary instead of crashing
process_incoming_stream(garbage_input)

```

---

## 🛠️ Core Blueprint Engine Architecture

When an input enters a function wrapped by `higi`, it passes through a 3-stage validation and correction pipeline:

1. **Structural Sanitization:** If the input is a raw string, `higi` evaluates the string boundaries and repairs broken structures (such as unclosed braces `{}` or brackets `[]`).
2. **Type Enforcement:** It maps the repaired data against your targeted configuration blueprint, automatically converting loose input types into matching Python primitives.
3. **Graceful Routing:** If structural anomalies are fully corrupted beyond repair, it automatically substitutes the input parameters with the preset fallback rules.

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

Created with 🧠 by [JANAPAREDDY GIRI SAI DURGA](https://www.google.com/search?q=https://github.com/sai8555)

```
---

### Why this works perfectly for your GitHub profile:
* **Professional Badges:** It includes professional dynamic shield badges at the top that show your current package build layout.
* **Code Blocks:** It has clean Python syntax highlighting so developers can copy your exact example script right into their text editors to test it out.
* **Pitch Perfect:** It hooks readers by contrasting it against standard rigid tools like Pydantic, proving why `higi` is a vital tool for modern AI developments. 

What do you think of this layout for your repository home?

```
