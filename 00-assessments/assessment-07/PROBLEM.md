# Assessment 7 -- Platform Coding Assessment (Linux, Apache, Microservices & API)

**Duration:** 90 minutes | **Total:** 100 marks | **Domain:** QuickTicket Event Booking
**Files:** `deploy.sh`, `quickticket.conf`, `openapi.yaml`, `payment-client.js`

---

## Instructions

- The QuickTicket platform team has reported defects in the deployment script, web server configuration, API specification, and microservice integration.
- Investigate and fix all issues.
- Fix only the 4 provided files
- Bash syntax for deploy.sh
- Apache 2.4 syntax for virtual host config
- OpenAPI 3.0.3 for YAML spec
- Node.js with axios for payment client
- Push all fixed files to your assigned branch before the timer ends.

---

## Question 1 -- Deployment Script Fixes [Simple] (30 marks)

The Bash deployment script `deploy.sh` has 4 issues reported by operations:

**DEF-101:** Running the script twice starts a second instance on the same port, causing a port conflict. The script should check if a previous instance is running and stop it first.

**DEF-102:** The script fails with "No such file or directory" when the log directory's parent does not exist. The directory creation should handle missing parent directories.

**DEF-103:** The application starts but cannot read its configuration because environment variables are not loaded. The `.env` file exists but is never sourced.

**DEF-104:** A new team member cannot run the script -- they get "Permission denied". Add a comment explaining correct file permissions for secure execution.

**Files to fix:** `deploy.sh`

---

## Question 2 -- Apache & OpenAPI Fixes [Medium] (35 marks)

**Apache config fixes (18 marks):** 3 issues in `quickticket.conf`:

**DEF-201:** API requests to `/api/events` return 404 through Apache even though the Node.js backend responds correctly on `localhost:3000`. The reverse proxy path matching is incorrect.

**DEF-202:** Navigating to `http://quickticket.local` does NOT redirect to HTTPS. The redirect rule exists but is in the wrong VirtualHost block.

**DEF-203:** Static files at `/var/www/quickticket/public/` return 403 Forbidden. The directory permissions configuration is blocking access.

**OpenAPI spec fixes (17 marks):** 4 issues in `openapi.yaml`:

**DEF-204:** The "Create Event" endpoint is documented as GET. Should be POST.

**DEF-205:** The Event response schema does not declare required fields.

**DEF-206:** The "Event not found" response is documented with status 200 instead of 404.

**DEF-207:** The request body is not marked as required and uses `text/plain` instead of `application/json`.

**Files to fix:** `quickticket.conf`, `openapi.yaml`

---

## Question 3 -- Microservice Client Fixes [Complex] (35 marks)

The payment service client `payment-client.js` has 3 resilience issues:

**DEF-301:** The payment service URL is hardcoded to `localhost:4000`. When deployed to staging or production, the client cannot reach the service. The URL should come from environment configuration.

**DEF-302:** If the payment service is slow, the order service waits indefinitely. There is no timeout configured on the HTTP calls.

**DEF-303:** When the payment service returns a 503 (Service Unavailable), the order service crashes with an unhandled exception. The client should handle errors gracefully and return a meaningful error to the caller.

**Files to fix:** `payment-client.js`

---

## Evaluation Parameters

| Parameter | Weightage |
|-----------|-----------|
| Ability to apply concepts and any additional functionality asked to implement | 20 |
| Coding Standards (Naming Conventions, Comments and Indentation) | 20 |
| Exception Handling | 20 |
| Completeness wrt Timelines as per requirements & Working application | 15 |
| Problem solving ability (think, evaluate and choose among alternates, and innovation/creativity) | 10 |
| Debugging / troubleshooting skills | 15 |
| **Total** | **100** |

---

## Submission

Push all fixed files to your assigned branch before the timer ends.
