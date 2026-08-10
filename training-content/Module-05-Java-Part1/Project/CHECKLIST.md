# Module 05 Checklist -- Participant Submission

## Bug Fixes
- [ ] Bug #1: MenuItem fields are private with proper getters/setters
- [ ] Bug #2: Order constructor initializes the items list (no NPE)
- [ ] Bug #3: totalAmount is an instance field (not static)
- [ ] Bug #4: Package imports compile correctly (no typos)

## Enhancements
- [ ] MenuItem has a meaningful toString() for logging
- [ ] MenuItem Builder pattern allows fluent construction
- [ ] equals() and hashCode() implemented based on item ID

## Debugging Evidence
- [ ] Screenshot of debugger showing static vs instance field values
- [ ] Brief description of how you traced the bug

## Self-Check Questions
1. What is the difference between `private`, `protected`, `public`, and default access?
2. Why should you initialize collections in the constructor?
3. What is the difference between a static field and an instance field?
4. Why do you need to override both `equals()` and `hashCode()` together?
5. What happens if you import from a package that does not exist?
