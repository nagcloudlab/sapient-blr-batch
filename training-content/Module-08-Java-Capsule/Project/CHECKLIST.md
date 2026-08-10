# Module 08 Checklist -- Participant Submission

## Bug Fixes
- [ ] FOOD-21: `GET /orders/{id}` returns order JSON (not 500) even when restaurant is missing
- [ ] FOOD-21: `GET /orders/99999` returns 404 (not 500)
- [ ] FOOD-23: `GET /orders` returns paginated results (default 10 per page)
- [ ] FOOD-23: `GET /orders?page=0&size=5` returns exactly 5 results
- [ ] FOOD-24: `POST /orders` with negative quantity returns 400 error

## Feature
- [ ] FOOD-22: `GET /orders?status=DELIVERED` returns only delivered orders
- [ ] FOOD-22: `GET /orders?status=PENDING` returns only pending orders
- [ ] FOOD-22: `GET /orders` without status param returns all orders

## Testing Evidence
- [ ] Postman collection or screenshots for each endpoint
- [ ] Tested both happy path and error cases

## Documentation
- [ ] Root-cause notes for FOOD-21 (why NullPointerException?)
- [ ] Root-cause notes for FOOD-23 (why no pagination?)
- [ ] Root-cause notes for FOOD-24 (why validation missing?)

## Self-Check Questions
1. What is the difference between `findAll()` and `findAll(Pageable)`?
2. Why should you return `Optional<T>` from service methods instead of null?
3. What does `@Valid` do on a controller method parameter?
4. What HTTP status code should a validation failure return?
5. Why is pagination important for APIs that return lists?
