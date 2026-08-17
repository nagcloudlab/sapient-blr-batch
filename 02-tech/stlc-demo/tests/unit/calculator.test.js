const {
  add,
  subtract,
  multiply,
  divide,
  percentage,
  toggleSign,
  calculate,
} = require("../../src/calculator");

// ─────────────────────────────────────────────
// US-01: Addition
// ─────────────────────────────────────────────
// Arrange
describe("add()", () => {
  test("adds two positive integers: 5 + 3 = 8", () => {
    const actual = add(5, 3); // Act
    const expected = 8;
    expect(actual).toBe(expected); // Assertion
  });

  test("adds two decimal numbers: 1.5 + 2.5 = 4", () => {
    expect(add(1.5, 2.5)).toBe(4);
  });

  test("adds to a previous result: 10 + 5 = 15", () => {
    expect(add(10, 5)).toBe(15);
  });

  test("adds zero: 7 + 0 = 7", () => {
    expect(add(7, 0)).toBe(7);
  });

  test("adds two negative numbers: -3 + -2 = -5", () => {
    expect(add(-3, -2)).toBe(-5);
  });

  test("adds negative and positive: -5 + 8 = 3", () => {
    expect(add(-5, 8)).toBe(3);
  });
});

// ─────────────────────────────────────────────
// US-02: Subtraction
// ─────────────────────────────────────────────
describe("subtract()", () => {
  test("subtracts two positive integers: 9 - 4 = 5", () => {
    expect(subtract(9, 4)).toBe(5);
  });

  test("result is negative: 3 - 7 = -4", () => {
    expect(subtract(3, 7)).toBe(-4);
  });

  test("subtracts decimals: 10.5 - 3.2 = 7.3", () => {
    expect(subtract(10.5, 3.2)).toBeCloseTo(7.3);
  });

  test("subtracts zero: 5 - 0 = 5", () => {
    expect(subtract(5, 0)).toBe(5);
  });

  test("subtracts from zero: 0 - 8 = -8", () => {
    expect(subtract(0, 8)).toBe(-8);
  });
});

// ─────────────────────────────────────────────
// US-03: Multiplication
// ─────────────────────────────────────────────
describe("multiply()", () => {
  test("multiplies two positive integers: 6 * 7 = 42", () => {
    expect(multiply(6, 7)).toBe(42);
  });

  test("multiplies by zero: 5 * 0 = 0", () => {
    expect(multiply(5, 0)).toBe(0);
  });

  test("multiplies decimals: 2.5 * 4 = 10", () => {
    expect(multiply(2.5, 4)).toBe(10);
  });

  test("multiplies by one: 9 * 1 = 9", () => {
    expect(multiply(9, 1)).toBe(9);
  });

  test("multiplies two negatives: -3 * -4 = 12", () => {
    expect(multiply(-3, -4)).toBe(12);
  });

  test("multiplies positive and negative: 6 * -2 = -12", () => {
    expect(multiply(6, -2)).toBe(-12);
  });
});

// ─────────────────────────────────────────────
// US-04: Division
// ─────────────────────────────────────────────
describe("divide()", () => {
  test("divides evenly: 8 / 2 = 4", () => {
    expect(divide(8, 2)).toBe(4);
  });

  test("divides with decimal result: 7 / 2 = 3.5", () => {
    expect(divide(7, 2)).toBe(3.5);
  });

  test("divides by one: 9 / 1 = 9", () => {
    expect(divide(9, 1)).toBe(9);
  });

  test("divides negative by positive: -10 / 2 = -5", () => {
    expect(divide(-10, 2)).toBe(-5);
  });

  test("divides zero by number: 0 / 5 = 0", () => {
    expect(divide(0, 5)).toBe(0);
  });
});

// ─────────────────────────────────────────────
// US-07: Division by Zero
// ─────────────────────────────────────────────
describe("divide() - division by zero", () => {
  test("5 / 0 returns 'Error'", () => {
    expect(divide(5, 0)).toBe("Error");
  });

  test("0 / 0 returns 'Error'", () => {
    expect(divide(0, 0)).toBe("Error");
  });

  test("-5 / 0 returns 'Error'", () => {
    expect(divide(-5, 0)).toBe("Error");
  });
});

// ─────────────────────────────────────────────
// US-09: Percentage
// ─────────────────────────────────────────────
describe("percentage()", () => {
  test("50% = 0.5", () => {
    expect(percentage(50)).toBe(0.5);
  });

  test("100% = 1", () => {
    expect(percentage(100)).toBe(1);
  });

  test("0% = 0", () => {
    expect(percentage(0)).toBe(0);
  });

  test("25% = 0.25", () => {
    expect(percentage(25)).toBe(0.25);
  });

  test("200% = 2", () => {
    expect(percentage(200)).toBe(2);
  });
});

// ─────────────────────────────────────────────
// US-08: Toggle Sign (+/-)
// ─────────────────────────────────────────────
describe("toggleSign()", () => {
  test("positive to negative: 5 becomes -5", () => {
    expect(toggleSign(5)).toBe(-5);
  });

  test("negative to positive: -5 becomes 5", () => {
    expect(toggleSign(-5)).toBe(5);
  });

  test("zero stays zero", () => {
    expect(toggleSign(0)).toBe(0);
  });

  test("decimal: 3.14 becomes -3.14", () => {
    expect(toggleSign(3.14)).toBe(-3.14);
  });
});

// ─────────────────────────────────────────────
// calculate() - Integration of all operations
// ─────────────────────────────────────────────
describe("calculate()", () => {
  test("calculate addition: 5 + 3 = 8", () => {
    expect(calculate(5, "+", 3)).toBe(8);
  });

  test("calculate subtraction: 9 - 4 = 5", () => {
    expect(calculate(9, "-", 4)).toBe(5);
  });

  test("calculate multiplication: 6 * 7 = 42", () => {
    expect(calculate(6, "*", 7)).toBe(42);
  });

  test("calculate division: 8 / 2 = 4", () => {
    expect(calculate(8, "/", 2)).toBe(4);
  });

  test("calculate division by zero: 5 / 0 = Error", () => {
    expect(calculate(5, "/", 0)).toBe("Error");
  });

  test("invalid operator returns Error", () => {
    expect(calculate(5, "^", 3)).toBe("Error");
  });

  test("string numbers are parsed correctly: '10' + '5' = 15", () => {
    expect(calculate("10", "+", "5")).toBe(15);
  });

  test("invalid input returns Error", () => {
    expect(calculate("abc", "+", "5")).toBe("Error");
  });

  test("decimal strings: '1.5' + '2.5' = 4", () => {
    expect(calculate("1.5", "+", "2.5")).toBe(4);
  });

  test("chained result: calculate(5, '*', 4) = 20", () => {
    expect(calculate(5, "*", 4)).toBe(20);
  });
});
