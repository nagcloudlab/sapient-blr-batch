# KEY TAKEAWAY: AI is a confident liar. Always verify. Never trust blindly.
# YOUR training is what makes you the verification layer.
# This is the ONLY module that uses BOTH models for comparison.

from config import banner, section, ask_both, pause, teaching_point

banner(11, "The Dark Side: When AI Fails",
       "AI is a confident liar — YOUR expertise is the verification layer")

# ---------------------------------------------------------------------------
# Concept
# ---------------------------------------------------------------------------
section("CONCEPT: AI hallucinations are NOT bugs — they're features")
print("""
LLMs generate text that is STATISTICALLY LIKELY, not FACTUALLY CORRECT.

The model doesn't "know" things. It predicts the next probable token.
When it doesn't know something, it DOESN'T say "I don't know."
It generates something that LOOKS right but IS wrong.

This is called HALLUCINATION.

THREE TYPES:
  1. FABRICATION:        Invents facts, versions, APIs that don't exist
  2. CONFABULATION:      Mixes up real things (right concept, wrong details)
  3. CONFIDENT NONSENSE: Explains fictional things with perfect confidence

WHY THIS IS DANGEROUS FOR ENGINEERS:
  - A hallucinated Docker image tag   -> broken build
  - A hallucinated K8s API version    -> deployment fails in production
  - A hallucinated security fix       -> vulnerability stays open
""")

pause(tip="This is the most important module. Let the danger sink in before demoing.")

# ---------------------------------------------------------------------------
# Test 1: Fabricated Kubernetes resource
# ---------------------------------------------------------------------------
section("TEST 1: Will the AI fabricate a Kubernetes resource?")

prompt1 = """Explain the Kubernetes `PodDisruptionSchedule` resource.
Include:
- What API group it belongs to
- A YAML example
- When to use it vs a PodDisruptionBudget"""

print("PROMPT: 'Explain the Kubernetes PodDisruptionSchedule resource'\n")
print(">>> NOTE TO STUDENTS: PodDisruptionSchedule does NOT EXIST.")
print("    It is completely made up. Watch what happens.\n")

ask_both(prompt1)

teaching_point("""
Did the models admit it doesn't exist, or did they fabricate it?

If they explained it confidently with YAML examples:
  THAT is a hallucination.
  YOUR K8s training is what tells you this resource is fake.
  Someone without your training would deploy this YAML and wonder why it fails.
""")

pause(tip="Ask: 'How many of you would have caught this without your K8s training?'")

# ---------------------------------------------------------------------------
# Test 2: Non-existent Docker image tag
# ---------------------------------------------------------------------------
section("TEST 2: Will the AI invent a Docker image version?")

prompt2 = """Write a Dockerfile using eclipse-temurin:17.0.42-jre-alpine as the base image.
Include a multi-stage build with Maven."""

print("PROMPT: 'Use eclipse-temurin:17.0.42-jre-alpine'\n")
print(">>> NOTE: Version 17.0.42 does NOT EXIST.")
print("    The latest 17.x is around 17.0.12.\n")

ask_both(prompt2)

teaching_point("""
Did the models use the fake version without questioning it?
In production, this Dockerfile would FAIL at 'docker build':

  ERROR: manifest for eclipse-temurin:17.0.42-jre-alpine not found

A 5-minute build failure at 2 AM because the AI made up a version.
ALWAYS verify version numbers against Docker Hub or official docs.
""")

pause()

# ---------------------------------------------------------------------------
# Test 3: Subtle security bugs
# ---------------------------------------------------------------------------
section("TEST 3: Can the AI spot subtle security vulnerabilities?")

prompt3 = """Review this Spring Boot controller for security issues.
Tell me if it's safe for production.

```java
@RestController
@RequestMapping("/api/returns")
public class ReturnController {

    @Autowired
    private ReturnService returnService;

    @GetMapping("/search")
    public ResponseEntity<List<Return>> searchReturns(
            @RequestParam String query) {
        String sql = "SELECT * FROM returns WHERE customer_name LIKE '%"
                     + query + "%' OR order_id = '" + query + "'";
        List<Return> results = returnService.executeQuery(sql);
        return ResponseEntity.ok(results);
    }

    @PostMapping("/process")
    public ResponseEntity<String> processReturn(
            @RequestBody ReturnRequest request) {
        String logMessage = "Processing return for: " + request.getCustomerName();
        log.info(logMessage);

        String cmd = "generate-label.sh " + request.getOrderId();
        Runtime.getRuntime().exec(cmd);

        returnService.processReturn(request);
        return ResponseEntity.ok("Return processed");
    }
}
```"""

print("PROMPT: 'Review this controller for security issues'\n")
print("HIDDEN BUGS (5 total):")
print("  1. SQL Injection     — string concatenation in query")
print("  2. Command Injection — Runtime.exec() with user input")
print("  3. Log Injection     — unsanitized user input in log")
print("  4. No input validation on any endpoint")
print("  5. No authentication/authorization checks\n")

ask_both(prompt3, max_tokens=2048)

teaching_point("""
SCORECARD:
  - How many of the 5 did each model catch?
  - Did either model MISS the command injection? (most dangerous one)
  - Did either model ADD a fake vulnerability? (hallucinating issues)

GPT-4o vs GPT-4o-mini: Which was more thorough?
  Bigger models generally catch more subtle issues.
  But NEITHER is a substitute for a security review by a trained human.
""")

pause()

# ---------------------------------------------------------------------------
# Test 4: Outdated configuration
# ---------------------------------------------------------------------------
section("TEST 4: Does the AI give outdated advice?")

prompt4 = """What is the correct way to configure MongoDB connection pooling
in Spring Boot 3.3 with the spring-boot-starter-data-mongodb dependency?

Show the application.yml configuration with:
- Connection pool minimum size: 10
- Connection pool maximum size: 100
- Connection timeout: 5000ms
- Max wait time: 10000ms"""

print("PROMPT: 'Configure MongoDB connection pooling in Spring Boot 3.3'\n")
print(">>> NOTE: Property names changed between Spring Boot 2.x and 3.x.")
print("    Common hallucination: mixing old and new property names.\n")

ask_both(prompt4)

teaching_point("""
Are the property names correct for Spring Boot 3.3?
  - spring.data.mongodb.* (3.x) vs spring.mongodb.* (2.x)?
  - Are these real properties or fabricated ones?

ALWAYS verify configuration against official documentation.
The AI might give you Spring Boot 2.x properties that SILENTLY
fail in 3.x — no error, just ignored. The worst kind of bug.
""")

pause()

# ---------------------------------------------------------------------------
# Reflection
# ---------------------------------------------------------------------------
section("THE CRITICAL LESSON")
print("""
Your 45-day training wasn't just about Docker, K8s, Jenkins, Ansible.
It was about building the JUDGMENT to verify AI-generated output.

  Without your training:
    "The AI said this Dockerfile is fine"
    -> Ship it -> Runs as root -> Security incident

  With your training:
    "The AI said it's fine, but I notice it runs as root and has
     no HEALTHCHECK"
    -> Fix it -> Ship it -> No incident

AI is a POWER TOOL. A chainsaw cuts faster than a handsaw.
But a chainsaw in untrained hands is dangerous.

  YOUR TRAINING = the safety certification.

RULES FOR USING AI IN PRODUCTION:
  1. Never trust AI output without verification
  2. Always check version numbers, API names, config keys
  3. Test AI-generated code BEFORE committing
  4. Use AI to DRAFT, then review like any other PR
  5. If it sounds too confident about something obscure — verify

Next up: YOUR turn. The Capstone Challenge.
""")

pause()
