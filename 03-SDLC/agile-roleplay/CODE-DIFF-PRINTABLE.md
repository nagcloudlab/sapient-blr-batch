# PR #347 -- Code Diff (Print 6 copies)

**Branch:** fix/cart-total-nan-on-coupon-remove
**Bug:** Cart total shows NaN when a coupon code is applied and then removed
**Author:** [Assigned PR Author in your group]
**Reviewers:** [Assigned Reviewer 1 and Reviewer 2 in your group]

---

```diff
File: src/cart/cartUtils.js

--- a/src/cart/cartUtils.js
+++ b/src/cart/cartUtils.js

@@ -12,14 +12,22 @@ function calculateCartTotal(items) {
   return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
 }

-function applyDiscount(total, coupon) {
-  if (coupon && coupon.discountPercent) {
-    return total - (total * coupon.discountPercent / 100);
-  }
-  return total;
+function applyDiscount(total, coupon) {
+  if (!coupon || coupon.discountPercent === undefined) {
+    return total;
+  }
+  const discount = total * coupon.discountPercent / 100;
+  return total - discount;
 }

 function getDisplayTotal(cartState) {
-  const raw = calculateCartTotal(cartState.items);
-  const discounted = applyDiscount(raw, cartState.activeCoupon);
-  return discounted;
+  if (!cartState || !cartState.items) {
+    return 0;
+  }
+  const raw = calculateCartTotal(cartState.items);
+  const discounted = applyDiscount(raw, cartState.activeCoupon);
+  console.log('Cart total calculated:', discounted);
+  return discounted;
 }

+// TODO: add coupon validation
+
 module.exports = { calculateCartTotal, applyDiscount, getDisplayTotal };
```

---

## Review Checklist (for reviewers)

- [ ] Is the bug fix correct?
- [ ] Are there any edge cases not handled?
- [ ] Is the code clean (no debug statements)?
- [ ] Are there unit tests for this change?
- [ ] Are there any TODOs that need follow-up?

## Your Decision (circle one):

**APPROVE** | **APPROVE WITH CHANGES** | **REQUEST CHANGES**

Reason: _______________________________________________________________
