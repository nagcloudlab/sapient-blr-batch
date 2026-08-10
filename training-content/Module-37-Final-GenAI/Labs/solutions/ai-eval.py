# FoodExpress AI Evaluation Harness -- FIXED VERSION

import openai
import os
import time
import logging
import re

# Fix 1: API key loaded from environment variable
API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    raise EnvironmentError("OPENAI_API_KEY environment variable is not set")

client = openai.OpenAI(api_key=API_KEY)

# Fix 5: Set up logging for audit trail
logging.basicConfig(
    filename="ai_audit.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("ai_eval")


def validate_output(text):
    """Fix 3: Validate AI output before returning."""
    # Check for prohibited content
    prohibited_patterns = [
        r"\b\d{10}\b",           # Phone numbers
        r"\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b",  # Card numbers
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Emails
        r"guaranteed|cure|heal|weight loss",  # Health claims
    ]
    for pattern in prohibited_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            logger.warning(f"Output validation failed: matched pattern '{pattern}'")
            return "[Description pending manual review -- prohibited content detected]"

    if len(text.split()) > 60:
        text = " ".join(text.split()[:50]) + "..."

    return text


def generate_menu_description(item_name, ingredients):
    """Generate a menu description using AI."""

    # Fix 6: No PII in prompt -- only item data
    prompt = f"""Generate a menu description for FoodExpress.
    Item: {item_name}
    Ingredients: {ingredients}
    """

    # Fix 2: Error handling around API call
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a food copywriter for FoodExpress. "
                        "Write appetizing descriptions in 2-3 sentences, under 50 words. "
                        "Do NOT include pricing, health claims, or allergen info."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )

        description = response.choices[0].message.content

        # Fix 3: Validate output
        validated = validate_output(description)

        # Fix 5: Log the AI response for audit
        logger.info(
            f"GENERATED | item={item_name} | "
            f"tokens={response.usage.total_tokens} | "
            f"output={validated[:100]}"
        )

        return validated

    except openai.APIError as e:
        logger.error(f"API error for {item_name}: {e}")
        return f"[Description unavailable -- API error]"
    except openai.RateLimitError as e:
        logger.error(f"Rate limit hit for {item_name}: {e}")
        return f"[Description unavailable -- rate limit reached]"
    except Exception as e:
        logger.error(f"Unexpected error for {item_name}: {e}")
        return f"[Description unavailable -- unexpected error]"


def batch_generate(items):
    """Generate descriptions for multiple menu items."""

    results = []
    # Fix 4: Rate limiting -- wait between API calls
    for i, item in enumerate(items):
        desc = generate_menu_description(item["name"], item["ingredients"])
        results.append({"name": item["name"], "description": desc})

        # Rate limit: max 10 calls per minute (wait 6 seconds between calls)
        if i < len(items) - 1:
            time.sleep(6)

    return results


if __name__ == "__main__":
    test_items = [
        {"name": "Chicken Biryani", "ingredients": "basmati rice, chicken, saffron, yogurt, onions"},
        {"name": "Masala Dosa", "ingredients": "rice batter, potato, mustard seeds, curry leaves"},
        {"name": "Paneer Tikka", "ingredients": "paneer, bell peppers, yogurt, tikka masala spice"},
    ]

    results = batch_generate(test_items)
    for r in results:
        print(f"{r['name']}: {r['description']}")
