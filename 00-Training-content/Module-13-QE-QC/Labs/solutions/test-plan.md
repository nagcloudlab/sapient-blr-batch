# FoodExpress Test Plan

## 1. Project Overview

**Application:** FoodExpress Food Delivery Platform
**Version:** 1.0
**Date:** July 2026
**Prepared by:** QE Team

## 2. Scope

### In Scope
- Cart functionality (add, remove, totals, discounts)
- Order lifecycle (place, confirm, dispatch, deliver, cancel)
- Restaurant menu browsing and search
- Delivery fee calculation

### Out of Scope
- Payment gateway integration (third-party)
- Push notifications
- Admin dashboard

## 3. Test Strategy

| Test Level       | Tool/Approach          | Responsibility     |
|------------------|------------------------|---------------------|
| Unit Testing     | Jest (JS), JUnit (Java)| Developers          |
| Integration      | Supertest / REST Assured| QE Team            |
| E2E / System     | Cypress / Selenium     | QE Team             |
| Performance      | JMeter / k6            | Performance Team    |

## 4. Test Cases

### 4.1 Cart Module

| TC ID  | Description                            | Steps                                              | Expected Result                        | Priority |
|--------|----------------------------------------|------------------------------------------------------|----------------------------------------|----------|
| TC-001 | Add item to empty cart                 | 1. Open app 2. Select restaurant 3. Add item        | Item appears in cart, quantity = 1      | High     |
| TC-002 | Add same item twice increases quantity | 1. Add item 2. Add same item again                   | Quantity = 2, single line item          | High     |
| TC-003 | Apply 10% discount                     | 1. Add items totalling 750 2. Apply 10% coupon       | Total = 675                            | High     |

### 4.2 Order Module

| TC ID  | Description                            | Steps                                              | Expected Result                        | Priority |
|--------|----------------------------------------|------------------------------------------------------|----------------------------------------|----------|
| TC-004 | Place order from cart                  | 1. Add items 2. Checkout 3. Confirm address          | Order status = "placed"                | Critical |
| TC-005 | Cancel a placed order                  | 1. Place order 2. Click Cancel                       | Order status = "cancelled"             | High     |
| TC-006 | Cannot cancel delivered order          | 1. Order marked delivered 2. Attempt cancel           | Error: "Cannot cancel delivered order" | Medium   |

## 5. Entry / Exit Criteria

### Entry Criteria
- Build deployed to QA environment successfully
- Unit test pass rate >= 90%
- Test data seeded in database

### Exit Criteria
- All Critical and High priority test cases pass
- No open Critical or Major defects
- Test coverage >= 80% for core modules

## 6. Defect Management

| Severity | Description                              | Example                                   |
|----------|------------------------------------------|--------------------------------------------|
| Critical | App crash or data loss                   | Order placed but not saved to database     |
| Major    | Feature broken, no workaround            | Discount calculation returns wrong amount  |
| Minor    | Cosmetic or low-impact issue             | Misaligned button on cart page             |

## 7. Risks and Mitigations

| Risk                              | Impact | Mitigation                             |
|-----------------------------------|--------|----------------------------------------|
| Third-party API downtime          | High   | Mock services for integration tests    |
| Incomplete test data              | Medium | Automated seed scripts for each run    |
| Environment instability           | Medium | Dockerized QA environment              |
