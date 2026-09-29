"""
Shared configuration for Gen-AI Prompt Engineering Training.
Uses OpenAI GPT-4o as the primary model.
"""

import os
import sys
from openai import OpenAI

# ---------------------------------------------------------------------------
# API Client
# ---------------------------------------------------------------------------
OPENAI_MODEL = "gpt-4o"
OPENAI_MODEL_MINI = "gpt-4o-mini"

def _get_openai_client():
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("[ERROR] Set OPENAI_API_KEY environment variable.")
        sys.exit(1)
    return OpenAI(api_key=key)

openai_client = _get_openai_client()

# ---------------------------------------------------------------------------
# Core helper: call a model and return the response
# ---------------------------------------------------------------------------
def ask(user_msg, system_msg="You are a helpful assistant.", temperature=0.3, max_tokens=2048, model=None):
    response = openai_client.chat.completions.create(
        model=model or OPENAI_MODEL,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
    )
    return response.choices[0].message.content

# ---------------------------------------------------------------------------
# Helper: call model and PRINT the response with a header
# ---------------------------------------------------------------------------
def ask_and_print(user_msg, system_msg="You are a helpful assistant.", temperature=0.3, max_tokens=2048, model=None, label=None):
    model_used = model or OPENAI_MODEL
    header = label or model_used
    print(f"\n{'='*70}")
    print(f"  {header}")
    print(f"{'='*70}\n")
    result = ask(user_msg, system_msg, temperature, max_tokens, model)
    print(result)
    return result

# ---------------------------------------------------------------------------
# Helper: call BOTH models side-by-side (used only in Module 11)
# ---------------------------------------------------------------------------
def ask_both(user_msg, system_msg="You are a helpful assistant.", temperature=0.3, max_tokens=2048):
    r1 = ask_and_print(user_msg, system_msg, temperature, max_tokens, model=OPENAI_MODEL, label="GPT-4o (powerful)")
    r2 = ask_and_print(user_msg, system_msg, temperature, max_tokens, model=OPENAI_MODEL_MINI, label="GPT-4o-mini (fast & cheap)")
    return r1, r2

# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------
def banner(module_num, title, takeaway):
    width = 70
    print("\n" + "#" * width)
    print(f"#  MODULE {module_num}: {title.upper()}")
    print(f"#  KEY TAKEAWAY: {takeaway}")
    print("#" * width + "\n")

def section(title):
    print(f"\n{'─' * 60}")
    print(f"  >>> {title}")
    print(f"{'─' * 60}\n")

def teaching_point(text):
    print(f"\n  {'*' * 50}")
    for line in text.strip().split("\n"):
        print(f"  *  {line.strip()}")
    print(f"  {'*' * 50}\n")

def pause(tip=None):
    if tip:
        print(f"\n  TEACHING TIP: {tip}")
    input("\n  [Press ENTER to continue...]\n")
