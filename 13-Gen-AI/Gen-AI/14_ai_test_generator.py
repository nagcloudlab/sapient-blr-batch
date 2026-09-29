# KEY TAKEAWAY: AI can generate comprehensive tests — but YOU must verify
# that the tests actually test the RIGHT things.

from config import banner, section, ask_and_print, ask, pause, teaching_point

banner(14, "AI Test Generator: From Code to JUnit 5",
       "Generate tests in seconds — but verify they test the RIGHT things")

# ---------------------------------------------------------------------------
# Concept
# ---------------------------------------------------------------------------
section("CONCEPT: AI + Testing = Superpower (with a catch)")
print("""
Writing tests is tedious. AI makes it fast. BUT:

  GOOD: AI generates boilerplate, setup, assertions in seconds
  BAD:  AI might test the WRONG things or miss critical edge cases

The pattern:
  1. AI generates the test skeleton (save 80% of time)
  2. YOU review for missing edge cases (the 20% that matters)
  3. YOU add domain-specific assertions (only you know the business rules)

This connects to your QE/QC training:
  - Test case design is a THINKING skill
  - AI handles the TYPING
  - You handle the THINKING
""")

pause(tip="Ask: 'How many of you skipped writing tests in your capsule projects?' (most will admit it)")

# ---------------------------------------------------------------------------
# Demo 1: Generate tests from a controller
# ---------------------------------------------------------------------------
section("DEMO 1: Generate JUnit 5 tests from a Spring Boot controller")

CODE_TO_TEST = """```java
@RestController
@RequestMapping("/api/returns")
@RequiredArgsConstructor
public class ReturnController {

    private final ReturnService returnService;

    @PostMapping
    public ResponseEntity<Return> createReturn(@Valid @RequestBody ReturnRequest request) {
        Return created = returnService.createReturn(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @PutMapping("/{id}/status")
    public ResponseEntity<Return> updateStatus(
            @PathVariable String id,
            @RequestParam ReturnStatus newStatus) {
        Return updated = returnService.updateStatus(id, newStatus);
        return ResponseEntity.ok(updated);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Return> getReturn(@PathVariable String id) {
        Return found = returnService.getReturnById(id);
        if (found == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(found);
    }

    @GetMapping("/customer/{customerId}")
    public ResponseEntity<Page<Return>> getByCustomer(
            @PathVariable String customerId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        Page<Return> returns = returnService.getReturnsByCustomer(customerId,
            PageRequest.of(page, size));
        return ResponseEntity.ok(returns);
    }
}
```"""

test_prompt = f"""Generate comprehensive JUnit 5 tests for this Spring Boot controller.

{CODE_TO_TEST}

REQUIREMENTS:
- Use MockMvc with @WebMvcTest
- Mock ReturnService with @MockBean
- Use @BeforeEach for common setup
- Test EACH endpoint with:
  a) Happy path (valid input, expected response)
  b) Edge case (boundary values, empty results)
  c) Error case (invalid input, not found, service exception)
- Use meaningful test method names: should_[expected]_when_[condition]
- Include proper assertions on HTTP status, response body, and headers
- Verify service method calls with Mockito verify()
- Add comments explaining WHAT each test validates and WHY

Generate the COMPLETE test class — ready to compile and run."""

SYSTEM = """You are a senior QE engineer at Publicis Sapient writing JUnit 5 tests
for a Spring Boot microservice. You follow these testing standards:
- Every endpoint needs happy path + edge case + error case
- Test names follow should_X_when_Y convention
- Every test has Arrange/Act/Assert sections clearly commented
- Mockito for service layer mocking
- AssertJ for fluent assertions where possible"""

print("Generating comprehensive JUnit 5 test suite...\n")
ask_and_print(test_prompt, system_msg=SYSTEM, max_tokens=4000, label="GENERATED TEST SUITE")

teaching_point("""
In 10 seconds, the AI generated a test class that would take
30-60 minutes to write manually.

BUT — review it critically:
  1. Did it test INVALID status transitions? (business logic)
  2. Did it test concurrent updates? (race conditions)
  3. Did it test pagination edge cases? (page beyond max)
  4. Did it verify the CORRECT exception types?
  5. Are the mock return values REALISTIC?

The AI writes the boilerplate. YOU add the business intelligence.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 2: Generate edge cases YOU might miss
# ---------------------------------------------------------------------------
section("DEMO 2: AI finds edge cases you didn't think of")

edge_prompt = f"""For this controller, identify edge cases that a junior developer would MISS
but a senior QE engineer would catch.

{CODE_TO_TEST}

For EACH edge case:
1. Describe the scenario
2. Why it's dangerous in production
3. The JUnit 5 test code to catch it

Focus on:
- State machine violations (invalid status transitions)
- Concurrency issues
- Input boundary values
- MongoDB-specific edge cases
- Security edge cases (authorization, injection)
- Pagination boundaries

List at least 8 edge cases, ordered by severity."""

print("Finding edge cases a junior developer would miss...\n")
ask_and_print(edge_prompt, system_msg=SYSTEM, max_tokens=3000, label="EDGE CASES")

teaching_point("""
THIS is the real value: AI as a THINKING PARTNER for test design.

Common edge cases developers miss:
  - What if customerId contains special chars? (NoSQL injection)
  - What if page=-1 or size=0?
  - What if the return is in REFUNDED status and you try to change to REQUESTED?
  - What if two requests update the same return simultaneously?
  - What if MongoDB is down during save?
  - What if the return ID is a valid ObjectId format but doesn't exist?

Your QE/QC training taught you to THINK about these.
AI helps you GENERATE the tests faster.
""")

pause()

# ---------------------------------------------------------------------------
# Demo 3: Generate tests for the Dockerfile
# ---------------------------------------------------------------------------
section("DEMO 3: Testing beyond code — Dockerfile tests")

dockerfile_test_prompt = """Generate a test script (using bash + container-structure-test or
similar approach) to validate a Dockerfile for a Spring Boot application.

Test these production requirements:
1. Image runs as non-root user (UID 1001)
2. No package manager (apt/apk) available in final image
3. HEALTHCHECK instruction exists
4. EXPOSE 8080 is set
5. JVM memory flags are configured (-Xms256m -Xmx512m)
6. Image size is under 200MB
7. No secrets or .env files in the image
8. The JAR file exists and is executable
9. The container starts and responds on /actuator/health within 30 seconds

Provide the tests as a container-structure-test YAML config
AND equivalent bash commands for those without the tool installed."""

print("Generating Dockerfile tests — infrastructure as testable code...\n")
ask_and_print(dockerfile_test_prompt, max_tokens=2000, label="DOCKERFILE TESTS")

teaching_point("""
Testing isn't just for Java code!

Your training covered Docker security hardening.
Now you can TEST those requirements automatically:
  - CI/CD runs these tests AFTER docker build
  - If image runs as root -> test fails -> build stops
  - If HEALTHCHECK missing -> test fails -> build stops
  - If image > 200MB -> test fails -> build stops

This is SHIFT-LEFT testing applied to infrastructure.
""")

pause()

# ---------------------------------------------------------------------------
# Reflection
# ---------------------------------------------------------------------------
section("AI TESTING WORKFLOW")
print("""
THE WORKFLOW:
  1. Write your code
  2. Ask AI to generate test suite         (saves 80% typing time)
  3. Ask AI to identify edge cases          (thinking partner)
  4. Review and add domain-specific tests   (YOUR expertise)
  5. Run tests in CI/CD pipeline            (automation)

WHAT AI IS GOOD AT:
  - Generating boilerplate (setup, teardown, mocks)
  - Standard edge cases (null, empty, boundary)
  - Multiple assertion styles (JUnit, AssertJ, Hamcrest)
  - Test naming conventions

WHAT AI IS BAD AT:
  - Business logic edge cases (state machine rules)
  - Integration test scenarios (real DB, real network)
  - Performance test thresholds (only you know your SLAs)
  - Security-specific test cases (OWASP-aware testing)

AI writes the skeleton. You add the soul.
""")

pause()
