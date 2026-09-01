# Module 14: Infrastructure -- Lab Setup

## Prerequisites

- No software installation required.
- A text editor or drawing tool (draw.io, Excalidraw, or paper) for diagrams.
- Access to `Labs/starter-code/` for the flawed infrastructure documents.

## Running the Starter Code

This is a document-based lab. There is no application to run.

1. Read `Project/BRIEF.md` for the full exercise instructions.
2. Open the files in `Labs/starter-code/` -- they contain an infrastructure diagram, HA design, and
   cost analysis sheet with deliberate errors.
3. Work through each issue listed in `lab-exercises.md`.

## Verifying Your Fixes

Compare your corrected documents against `Project/CHECKLIST.md`:

- Infrastructure map: all FoodExpress components are present, connections are labelled.
- HA design: single points of failure are identified and mitigated.
- Cost analysis: correct instance sizing, data transfer costs included, reserved vs. on-demand reasoning.

## Expected Behavior

- Infrastructure diagram shows frontend, API gateway, microservices, databases, and CDN.
- HA design includes redundancy at every tier (load balancer, app, database).
- Cost estimate is within 10% of the reference figure in `SOLUTION.md`.
- No single service failure brings down the entire application.

## Troubleshooting

**Unsure what counts as a single point of failure:** Any component with no standby or replica is an
SPOF. Common examples: a single database instance, a single availability zone, no load balancer.

**Cost analysis totals do not match:** Check that you are using the same cloud region and pricing tier
as specified in `BRIEF.md`. Data egress costs are a frequent omission.
