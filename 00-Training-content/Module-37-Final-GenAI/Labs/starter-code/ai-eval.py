# FoodExpress AI Evaluation Harness
# THIS FILE CONTAINS 6 BUGS -- Find and fix them all!

import openai

# Bug 1: API key hardcoded in source code
API_KEY = "sk-abc123def456ghi789jkl012mno345pqr678stu901vwx"

client = openai.OpenAI(api_key=API_KEY)


def generate_menu_description(item_name, ingredients):
    """Generate a menu description using AI."""

    # Bug 6: Customer data included without PII redaction
    prompt = f"""Generate a menu description for FoodExpress.
    Item: {item_name}
    Ingredients: {ingredients}
    Customer who requested: Priya Sharma, phone: +91-9876543210,
    address: 42 MG Road, Bangalore 560001
    """

    # Bug 2: No error handling around API call
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Generate menu descriptions."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.7
    )

    description = response.choices[0].message.content

    # Bug 3: No output validation
    # Bug 5: No logging of AI response
    return description


def batch_generate(items):
    """Generate descriptions for multiple menu items."""

    results = []
    # Bug 4: No rate limiting -- calls API as fast as possible
    for item in items:
        desc = generate_menu_description(item["name"], item["ingredients"])
        results.append({"name": item["name"], "description": desc})

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
