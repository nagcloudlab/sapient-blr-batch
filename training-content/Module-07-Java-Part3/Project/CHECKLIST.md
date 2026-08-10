# Module 07 Checklist -- Participant Submission

## Bug Fixes
- [ ] Bug #1: Cart items removed safely without ConcurrentModificationException
- [ ] Bug #2: Cuisine categories have no duplicates (Set used instead of List)
- [ ] Bug #3: All collections use generics (no raw types, no unsafe casts)
- [ ] Bug #4: JDBC connections, statements, and result sets are properly closed

## Enhancements
- [ ] Safe removal uses removeIf() or Iterator.remove()
- [ ] All SQL queries use PreparedStatement with parameters (no string concatenation)
- [ ] JDBC resources wrapped in try-with-resources

## Debugging Evidence
- [ ] Screenshot of stack trace for ConcurrentModificationException
- [ ] Brief description of how you identified and fixed the issue

## Self-Check Questions
1. Why does modifying a collection during for-each iteration throw an exception?
2. What is the difference between ArrayList, HashSet, and LinkedHashSet?
3. Why are raw types (e.g., `List` without `<Type>`) considered unsafe?
4. What happens if you never close a JDBC Connection?
5. How does PreparedStatement prevent SQL injection?
