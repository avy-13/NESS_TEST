# Automation E2E Framework – Playwright + Pytest

## Overview
This project is an end-to-end automation framework built as part of a senior automation engineering assignment.

The framework validates core e-commerce flows on AliExpress:
- Authentication
- Product search
- Price filtering (low → high)
- Adding products to cart
- Cart total validation

The solution emphasizes:
- Clean architecture
- Scalability
- Stability
- Data-driven testing
- CI readiness

---

## Architecture


├── config/ # Environment & execution config
├── data/ # Test data (Data-Driven)
├── pages/ # Page Object Model
├── tests/ # Test scenarios
├── utils/ # Reusable helpers
├── .github/ # GitHub Actions CI
├── conftest.py # Pytest fixtures
└── README.md


---

## 🧠 Design Principles

- **Page Object Model** – UI logic isolated from tests
- **Single Responsibility** – Each class handles one concern
- **Data-Driven** – No hardcoded values in tests
- **Robust Locators** – Fallback locators with retries
- **Session Isolation** – New browser context per test

---

## Execution & Performance

### Parallel Execution
Tests are executed in parallel using `pytest-xdist`:

```bash
pytest -n auto
