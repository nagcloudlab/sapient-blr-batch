"""
Setup Check: Verify OpenAI API key is configured and working.
Run this FIRST before the training session.
"""

import os

def check():
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        print("[FAIL] OPENAI_API_KEY not set")
        print("\nRun: export OPENAI_API_KEY='your-key-here'")
        return False

    from openai import OpenAI
    client = OpenAI(api_key=key)

    for model in ["gpt-4o", "gpt-4o-mini"]:
        try:
            r = client.chat.completions.create(
                model=model,
                max_tokens=20,
                messages=[{"role": "user", "content": "Say OK"}],
            )
            print(f"[PASS] {model:15s} -> {r.choices[0].message.content.strip()}")
        except Exception as e:
            print(f"[FAIL] {model:15s} -> {e}")
            return False

    print("\nAll systems go! Ready for training.")
    return True

if __name__ == "__main__":
    check()
