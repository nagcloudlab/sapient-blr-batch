# KEY TAKEAWAY: You can build an AI code reviewer that reviews code
# the way YOUR team reviews code — with YOUR standards, YOUR rubric, YOUR tone.

import json
from config import banner, section, ask_and_print, ask, pause, teaching_point

banner(13, "AI Code Reviewer: Your Standards, Your Rules",
       "Build a reviewer that thinks like YOUR senior engineer")

# ---------------------------------------------------------------------------
# Concept
# ---------------------------------------------------------------------------
section("CONCEPT: Why not just ask 'review my code'?")
print("""
You've seen me review your capsule projects for 45 days.
Every review followed a CONSISTENT pattern:

  1. Architecture — Does the design make sense?
  2. Code quality — Naming, structure, separation of concerns?
  3. Security    — Injection, auth, secrets management?
  4. DevOps      — Dockerfile, K8s, CI/CD pipeline quality?
  5. Testing     — Coverage, edge cases, assertions?
  6. Scoring     — Out of 100 with specific criteria

ChatGPT doesn't know this rubric. But we can TEACH it.
We'll build a code reviewer that reviews EXACTLY like our team.
""")

pause(tip="Ask: 'What made a capsule review helpful vs not helpful? What pattern did you notice?'")

# ---------------------------------------------------------------------------
# Demo 1: The team's review standards (system prompt)
# ---------------------------------------------------------------------------
section("DEMO 1: Defining YOUR team's review standards")

REVIEWER_SYSTEM = """You are a senior engineer at Publicis Sapient reviewing a junior developer's
capsule project submission. You have reviewed 27 submissions in the past 45 days
and you follow this EXACT scoring rubric:

SCORING RUBRIC (100 points total):
  - Ability to apply concepts:          20 points
  - Coding standards (naming, comments): 15 points
  - Exception handling:                  20 points
  - Completeness & working application: 15 points
  - Problem-solving ability:            10 points
  - Debugging/troubleshooting skills:   10 points
  - Security best practices:            10 points

REVIEW FORMAT:
For each category, provide:
  1. Score out of max points
  2. What was done WELL (be specific, cite line numbers)
  3. What needs IMPROVEMENT (be specific, show the fix)
  4. One ACTIONABLE recommendation

TONE:
  - Be encouraging but honest
  - Highlight strengths BEFORE weaknesses
  - Every criticism must come with a concrete fix
  - End with "Next Steps" — 3 specific things to improve

You are reviewing a Spring Boot microservice for a Return & Refund platform."""

print("SYSTEM PROMPT: Your team's exact review rubric + scoring + tone\n")
print("This system prompt encodes:")
print("  - The 100-point scoring rubric from your training")
print("  - The review format (score + good + improve + action)")
print("  - The tone (encouraging but honest)")
print("  - The domain context (Return & Refund platform)")

pause()

# ---------------------------------------------------------------------------
# Demo 2: Review a realistic Spring Boot service
# ---------------------------------------------------------------------------
section("DEMO 2: Review a capsule project submission")

SAMPLE_CODE = """
```java
// ReturnService.java
@Service
public class ReturnService {

    @Autowired
    MongoTemplate mongoTemplate;

    public Return createReturn(ReturnRequest req) {
        Return r = new Return();
        r.setCustomerName(req.getCustomerName());
        r.setOrderId(req.getOrderId());
        r.setReason(req.getReason());
        r.setStatus("REQUESTED");
        r.setCreatedAt(new Date());
        mongoTemplate.save(r);
        return r;
    }

    public Return updateStatus(String id, String status) {
        Return r = mongoTemplate.findById(id, Return.class);
        r.setStatus(status);
        r.setUpdatedAt(new Date());
        mongoTemplate.save(r);
        return r;
    }

    public List<Return> getReturnsByCustomer(String name) {
        Query q = new Query(Criteria.where("customerName").is(name));
        return mongoTemplate.find(q, Return.class);
    }

    public void deleteReturn(String id) {
        mongoTemplate.remove(new Query(Criteria.where("id").is(id)), Return.class);
    }
}
```

```java
// ReturnController.java
@RestController
@RequestMapping("/api/returns")
public class ReturnController {

    @Autowired
    ReturnService returnService;

    @PostMapping
    public Return create(@RequestBody ReturnRequest req) {
        return returnService.createReturn(req);
    }

    @PutMapping("/{id}/status")
    public Return updateStatus(@PathVariable String id, @RequestParam String status) {
        return returnService.updateStatus(id, status);
    }

    @GetMapping("/customer/{name}")
    public List<Return> getByCustomer(@PathVariable String name) {
        return returnService.getReturnsByCustomer(name);
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable String id) {
        returnService.deleteReturn(id);
    }
}
```
"""

review_prompt = f"""Review this capsule project submission using the scoring rubric.

SUBMISSION: Return Service — Spring Boot + MongoDB
STUDENT: (anonymous)
MODULE: Microservices & Backend Development

{SAMPLE_CODE}

Provide your complete review with:
1. Score breakdown per category (out of 100)
2. Detailed feedback per category
3. Overall assessment
4. Next Steps (3 specific improvements)"""

print("Reviewing a realistic capsule submission...\n")
ask_and_print(review_prompt, system_msg=REVIEWER_SYSTEM, max_tokens=2048, label="AI CODE REVIEW")

teaching_point("""
This review follows YOUR rubric — the same one used for 45 days.

NOTICE what the AI catches:
  - No exception handling (updateStatus will NPE if ID not found)
  - No input validation
  - No ResponseEntity with proper HTTP status codes
  - No @Valid annotation
  - Hard-delete instead of soft-delete
  - No pagination on getByCustomer
  - Direct field injection (@Autowired) instead of constructor injection

These are EXACTLY the issues found in real capsule reviews.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 3: Comparative review (before/after)
# ---------------------------------------------------------------------------
section("DEMO 3: Review the IMPROVED version")

IMPROVED_CODE = """
```java
// ReturnService.java (improved)
@Service
@RequiredArgsConstructor
public class ReturnService {

    private final MongoTemplate mongoTemplate;

    public Return createReturn(@Valid ReturnRequest req) {
        Return r = Return.builder()
            .customerName(req.getCustomerName())
            .orderId(req.getOrderId())
            .reason(req.getReason())
            .status(ReturnStatus.REQUESTED)
            .createdAt(Instant.now())
            .build();

        try {
            return mongoTemplate.save(r);
        } catch (DataAccessException e) {
            throw new ServiceException("Failed to create return", e);
        }
    }

    public Return updateStatus(String id, ReturnStatus newStatus) {
        Return r = mongoTemplate.findById(id, Return.class);
        if (r == null) {
            throw new ResourceNotFoundException("Return not found: " + id);
        }

        // Validate state transition
        if (!r.getStatus().canTransitionTo(newStatus)) {
            throw new InvalidStateException(
                "Cannot transition from " + r.getStatus() + " to " + newStatus);
        }

        r.setStatus(newStatus);
        r.setUpdatedAt(Instant.now());
        return mongoTemplate.save(r);
    }

    public Page<Return> getReturnsByCustomer(String name, Pageable pageable) {
        Query q = new Query(Criteria.where("customerName").is(name)).with(pageable);
        List<Return> results = mongoTemplate.find(q, Return.class);
        long count = mongoTemplate.count(Query.query(Criteria.where("customerName").is(name)), Return.class);
        return new PageImpl<>(results, pageable, count);
    }
}
```
"""

compare_prompt = f"""Now review this IMPROVED version of the same service.
Compare it with the original and highlight what improved.

{IMPROVED_CODE}

Score it using the same rubric. Show the score IMPROVEMENT from the original."""

print("Reviewing the improved version for comparison...\n")
ask_and_print(compare_prompt, system_msg=REVIEWER_SYSTEM, max_tokens=2048, label="IMPROVED CODE REVIEW")

teaching_point("""
The AI reviewer caught the improvements:
  - Constructor injection instead of @Autowired
  - Exception handling with custom exceptions
  - Input validation with @Valid
  - State machine validation (canTransitionTo)
  - Pagination for list queries
  - Instant instead of Date
  - Builder pattern
  - Soft-delete (removed the hard delete endpoint)

THIS is how you build a CI/CD code review bot:
  1. System prompt = your team's standards + rubric
  2. User prompt = the PR diff
  3. Output = structured review with scores
  4. Integrate with GitHub Actions or Jenkins
""")

pause()

# ---------------------------------------------------------------------------
# Reflection
# ---------------------------------------------------------------------------
section("BUILD YOUR OWN REVIEWER")
print("""
To build a code reviewer for YOUR team:

  1. SYSTEM PROMPT: Your coding standards, rubric, tone
  2. FEW-SHOT:      2-3 examples of past reviews you liked
  3. FORMAT:         Score breakdown + specific feedback + fixes
  4. CONSTRAINTS:    "Every criticism must include the corrected code"

This could be:
  - A GitHub Actions bot that reviews every PR
  - A Jenkins stage that scores code quality
  - A pre-commit hook that catches issues before push
  - A training tool for new joiners to practice

The AI reviewer is CONSISTENT — it applies the SAME rubric every time.
Unlike humans, it doesn't have bad days or skip reviews when busy.
""")

pause()
