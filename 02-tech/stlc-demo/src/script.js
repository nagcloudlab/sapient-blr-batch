// UI Controller - wires DOM to calculator logic
(function () {
  let currentInput = "0";
  let previousInput = "";
  let operator = null;
  let shouldResetDisplay = false;

  const display = document.getElementById("display");

  function updateDisplay(value) {
    display.textContent = value;
  }

  function handleNumber(value) {
    if (currentInput === "Error") currentInput = "0";
    if (shouldResetDisplay) {
      currentInput = "0";
      shouldResetDisplay = false;
    }
    if (currentInput === "0" && value !== ".") {
      currentInput = value;
    } else {
      currentInput += value;
    }
    updateDisplay(currentInput);
  }

  function handleDecimal() {
    if (shouldResetDisplay) {
      currentInput = "0";
      shouldResetDisplay = false;
    }
    if (!currentInput.includes(".")) {
      currentInput += ".";
      updateDisplay(currentInput);
    }
  }

  function handleOperator(nextOperator) {
    const current = parseFloat(currentInput);

    if (operator && !shouldResetDisplay) {
      const prev = parseFloat(previousInput);
      let result;
      if (operator === "/" && current === 0) {
        result = "Error";
      } else {
        switch (operator) {
          case "+": result = prev + current; break;
          case "-": result = prev - current; break;
          case "*": result = prev * current; break;
          case "/": result = prev / current; break;
        }
      }
      currentInput = String(result);
      updateDisplay(currentInput);
    }

    previousInput = currentInput;
    operator = nextOperator;
    shouldResetDisplay = true;
  }

  function handleEquals() {
    if (!operator) return;
    const prev = parseFloat(previousInput);
    const current = parseFloat(currentInput);
    let result;

    if (operator === "/" && current === 0) {
      result = "Error";
    } else {
      switch (operator) {
        case "+": result = prev + current; break;
        case "-": result = prev - current; break;
        case "*": result = prev * current; break;
        case "/": result = prev / current; break;
      }
    }

    currentInput = String(result);
    operator = null;
    previousInput = "";
    shouldResetDisplay = true;
    updateDisplay(currentInput);
  }

  function handleClear() {
    currentInput = "0";
    previousInput = "";
    operator = null;
    shouldResetDisplay = false;
    updateDisplay("0");
  }

  function handleToggleSign() {
    if (currentInput === "Error" || currentInput === "0") return;
    currentInput = String(-parseFloat(currentInput));
    updateDisplay(currentInput);
  }

  function handlePercentage() {
    currentInput = String(parseFloat(currentInput) / 100);
    updateDisplay(currentInput);
  }

  document.querySelector(".buttons").addEventListener("click", (e) => {
    const btn = e.target.closest(".btn");
    if (!btn) return;

    const action = btn.dataset.action;
    const value = btn.dataset.value;

    switch (action) {
      case "number": handleNumber(value); break;
      case "decimal": handleDecimal(); break;
      case "operator": handleOperator(value); break;
      case "equals": handleEquals(); break;
      case "clear": handleClear(); break;
      case "toggleSign": handleToggleSign(); break;
      case "percentage": handlePercentage(); break;
    }
  });
})();
