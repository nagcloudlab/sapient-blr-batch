const { test, expect } = require("@playwright/test");
const CALC_URL = "http://127.0.0.1:5500/src/index.html";

// Helper: click a sequence of calculator buttons
async function pressButtons(page, ...buttons) {
  for (const btn of buttons) {
    if (["+", "-", "*", "/"].includes(btn)) {
      await page.click(`button[data-action="operator"][data-value="${btn}"]`);
    } else if (btn === "=") {
      await page.click('button[data-action="equals"]');
    } else if (btn === "AC") {
      await page.click('button[data-action="clear"]');
    } else if (btn === ".") {
      await page.click('button[data-action="decimal"]');
    } else if (btn === "+/-") {
      await page.click('button[data-action="toggleSign"]');
    } else if (btn === "%") {
      await page.click('button[data-action="percentage"]');
    } else {
      await page.click(`button[data-action="number"][data-value="${btn}"]`);
    }
  }
}

// Helper: get display text
async function getDisplay(page) {
  return await page.textContent("#display");
}

// ─────────────────────────────────────────────
// Initial State
// ─────────────────────────────────────────────
test.describe("Initial State", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(CALC_URL);
  });

  test("display shows 0 on load", async ({ page }) => {
    expect(await getDisplay(page)).toBe("0");
  });

  test("all buttons are visible", async ({ page }) => {
    const buttons = await page.locator(".btn").count();
    expect(buttons).toBe(19); // 10 digits + 4 operators + AC + +/- + % + . + =
  });
});

// ─────────────────────────────────────────────
// US-01: Addition
// ─────────────────────────────────────────────
test.describe("US-01: Addition", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(CALC_URL);
  });

  test("5 + 3 = 8", async ({ page }) => {
    await pressButtons(page, "5", "+", "3", "=");
    expect(await getDisplay(page)).toBe("8");
  });

  test("1.5 + 2.5 = 4", async ({ page }) => {
    await pressButtons(page, "1", ".", "5", "+", "2", ".", "5", "=");
    expect(await getDisplay(page)).toBe("4");
  });

  test("chained: result 10 + 5 = 15", async ({ page }) => {
    await pressButtons(page, "6", "+", "4", "="); // result = 10
    await pressButtons(page, "+", "5", "=");
    expect(await getDisplay(page)).toBe("15");
  });

  test("0 + 0 = 0", async ({ page }) => {
    await pressButtons(page, "0", "+", "0", "=");
    expect(await getDisplay(page)).toBe("0");
  });
});

// ─────────────────────────────────────────────
// US-02: Subtraction
// ─────────────────────────────────────────────
test.describe("US-02: Subtraction", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(CALC_URL);
  });

  test("9 - 4 = 5", async ({ page }) => {
    await pressButtons(page, "9", "-", "4", "=");
    expect(await getDisplay(page)).toBe("5");
  });

  test("3 - 7 = -4", async ({ page }) => {
    await pressButtons(page, "3", "-", "7", "=");
    expect(await getDisplay(page)).toBe("-4");
  });

  test("10.5 - 3.2 = 7.3", async ({ page }) => {
    await pressButtons(page, "1", "0", ".", "5", "-", "3", ".", "2", "=");
    expect(await getDisplay(page)).toBe("7.3");
  });

  test("5 - 0 = 5", async ({ page }) => {
    await pressButtons(page, "5", "-", "0", "=");
    expect(await getDisplay(page)).toBe("5");
  });
});

// ─────────────────────────────────────────────
// US-03: Multiplication
// ─────────────────────────────────────────────
test.describe("US-03: Multiplication", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(CALC_URL);
  });

  test("6 * 7 = 42", async ({ page }) => {
    await pressButtons(page, "6", "*", "7", "=");
    expect(await getDisplay(page)).toBe("42");
  });

  test("5 * 0 = 0", async ({ page }) => {
    await pressButtons(page, "5", "*", "0", "=");
    expect(await getDisplay(page)).toBe("0");
  });

  test("2.5 * 4 = 10", async ({ page }) => {
    await pressButtons(page, "2", ".", "5", "*", "4", "=");
    expect(await getDisplay(page)).toBe("10");
  });
});

// ─────────────────────────────────────────────
// US-04: Division
// ─────────────────────────────────────────────
test.describe("US-04: Division", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(CALC_URL);
  });

  test("8 / 2 = 4", async ({ page }) => {
    await pressButtons(page, "8", "/", "2", "=");
    expect(await getDisplay(page)).toBe("4");
  });

  test("7 / 2 = 3.5", async ({ page }) => {
    await pressButtons(page, "7", "/", "2", "=");
    expect(await getDisplay(page)).toBe("3.5");
  });

  test("5 / 0 = Error", async ({ page }) => {
    await pressButtons(page, "5", "/", "0", "=");
    expect(await getDisplay(page)).toBe("Error");
  });
});

// ─────────────────────────────────────────────
// US-05: Clear (AC)
// ─────────────────────────────────────────────
test.describe("US-05: Clear Calculator", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(CALC_URL);
  });

  test("AC resets display to 0 after entering number", async ({ page }) => {
    await pressButtons(page, "1", "2", "3");
    expect(await getDisplay(page)).toBe("123");
    await pressButtons(page, "AC");
    expect(await getDisplay(page)).toBe("0");
  });

  test("AC clears partial expression", async ({ page }) => {
    await pressButtons(page, "5", "+");
    await pressButtons(page, "AC");
    expect(await getDisplay(page)).toBe("0");
  });

  test("AC resets after Error", async ({ page }) => {
    await pressButtons(page, "5", "/", "0", "=");
    expect(await getDisplay(page)).toBe("Error");
    await pressButtons(page, "AC");
    expect(await getDisplay(page)).toBe("0");
  });
});

// ─────────────────────────────────────────────
// US-06: Decimal Numbers
// ─────────────────────────────────────────────
test.describe("US-06: Decimal Numbers", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(CALC_URL);
  });

  test("pressing . at start shows 0.", async ({ page }) => {
    await pressButtons(page, ".");
    expect(await getDisplay(page)).toBe("0.");
  });

  test("second decimal point is ignored", async ({ page }) => {
    await pressButtons(page, "3", ".", "1", "4", ".");
    expect(await getDisplay(page)).toBe("3.14");
  });

  test("0.5 + 0.5 = 1", async ({ page }) => {
    await pressButtons(page, ".", "5", "+", ".", "5", "=");
    expect(await getDisplay(page)).toBe("1");
  });
});

// ─────────────────────────────────────────────
// US-07: Division by Zero
// ─────────────────────────────────────────────
test.describe("US-07: Division by Zero", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(CALC_URL);
  });

  test("5 / 0 shows Error", async ({ page }) => {
    await pressButtons(page, "5", "/", "0", "=");
    expect(await getDisplay(page)).toBe("Error");
  });

  test("AC after Error resets to 0", async ({ page }) => {
    await pressButtons(page, "5", "/", "0", "=");
    await pressButtons(page, "AC");
    expect(await getDisplay(page)).toBe("0");
  });

  test("digit after Error resets calculator", async ({ page }) => {
    await pressButtons(page, "5", "/", "0", "=");
    expect(await getDisplay(page)).toBe("Error");
    await pressButtons(page, "7");
    expect(await getDisplay(page)).toBe("7");
  });
});

// ─────────────────────────────────────────────
// US-08: Toggle Sign (+/-)
// ─────────────────────────────────────────────
test.describe("US-08: Toggle Sign", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(CALC_URL);
  });

  test("5 becomes -5", async ({ page }) => {
    await pressButtons(page, "5", "+/-");
    expect(await getDisplay(page)).toBe("-5");
  });

  test("-5 becomes 5", async ({ page }) => {
    await pressButtons(page, "5", "+/-", "+/-");
    expect(await getDisplay(page)).toBe("5");
  });

  test("0 stays 0 (no -0)", async ({ page }) => {
    await pressButtons(page, "+/-");
    expect(await getDisplay(page)).toBe("0");
  });
});

// ─────────────────────────────────────────────
// US-09: Percentage
// ─────────────────────────────────────────────
test.describe("US-09: Percentage", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(CALC_URL);
  });

  test("50% = 0.5", async ({ page }) => {
    await pressButtons(page, "5", "0", "%");
    expect(await getDisplay(page)).toBe("0.5");
  });

  test("100% = 1", async ({ page }) => {
    await pressButtons(page, "1", "0", "0", "%");
    expect(await getDisplay(page)).toBe("1");
  });

  test("0% = 0", async ({ page }) => {
    await pressButtons(page, "%");
    expect(await getDisplay(page)).toBe("0");
  });
});

// ─────────────────────────────────────────────
// US-10: Chained Operations
// ─────────────────────────────────────────────
test.describe("US-10: Chained Operations", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(CALC_URL);
  });

  test("2 + 3 * → display shows 5 (evaluates before next op)", async ({ page }) => {
    await pressButtons(page, "2", "+", "3", "*");
    expect(await getDisplay(page)).toBe("5");
  });

  test("2 + 3 * 4 = 20", async ({ page }) => {
    await pressButtons(page, "2", "+", "3", "*", "4", "=");
    expect(await getDisplay(page)).toBe("20");
  });

  test("10 - 3 + 2 = 9", async ({ page }) => {
    await pressButtons(page, "1", "0", "-", "3", "+", "2", "=");
    expect(await getDisplay(page)).toBe("9");
  });
});

// ─────────────────────────────────────────────
// FR-02: Digit Input Edge Cases
// ─────────────────────────────────────────────
test.describe("Digit Input Edge Cases", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(CALC_URL);
  });

  test("no leading zeros: pressing 0, 0, 7 shows 7", async ({ page }) => {
    await pressButtons(page, "0", "0", "7");
    expect(await getDisplay(page)).toBe("7");
  });

  test("multi-digit number: 123", async ({ page }) => {
    await pressButtons(page, "1", "2", "3");
    expect(await getDisplay(page)).toBe("123");
  });

  test("pressing = without operator shows current number", async ({ page }) => {
    await pressButtons(page, "5", "=");
    expect(await getDisplay(page)).toBe("5");
  });

  test("pressing operator without first number uses 0", async ({ page }) => {
    await pressButtons(page, "+", "5", "=");
    expect(await getDisplay(page)).toBe("5");
  });
});
