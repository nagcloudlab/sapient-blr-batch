# Module 09: Node.js (Part 1) -- Restaurant Service Bugs

## Sustain Context

The client escalated:

> "We are building a new Restaurant Service in Node.js. The previous developer left and the code has issues -- modules are not loading, callbacks are nested five levels deep, promises are rejecting silently, and the file paths break on the server. We need this service listing restaurants and reading menus from JSON files by end of day."

---

## Tasks

| # | Type | Issue | File |
|---|------|-------|------|
| 1 | BUG | Missing or wrong `require()` calls crash on startup | `server.js`, `utils/logger.js` |
| 2 | BUG | Callback hell in menu loader -- unreadable and error-prone | `services/menuLoader.js` |
| 3 | BUG | Unhandled promise rejection crashes the process | `services/restaurantService.js` |
| 4 | BUG | File path uses hardcoded `\` separator -- fails on Linux server | `services/menuLoader.js` |
| 5 | ENH | List all restaurants from `data/restaurants.json` | `services/restaurantService.js` |
| 6 | ENH | Read menu for a restaurant from `data/menus/{id}.json` | `services/menuLoader.js` |

## Deliverables

- [ ] All 4 bugs fixed, 2 enhancements working
- [ ] `node server.js` starts without errors
- [ ] Restaurant list and menu data load correctly from JSON files
- [ ] Brief root-cause notes for each bug
