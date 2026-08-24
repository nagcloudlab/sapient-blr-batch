# Agile Role Play -- Facilitation Guide

**Date:** Fri Aug 21, 2026 | **Day 18** | **Duration:** 70 min
**Topics Covered:** Infra, SDLC, Jira/Confluence, DevOps, Git, CI/CD
**Batch:** 27 participants | **Groups:** 6 (4-5 per group)

---

## WHAT ARE WE DOING?

Two back-to-back activities that simulate what an engineering team does every day:

| Round | Activity | What It Tests | Time |
|-------|----------|--------------|------|
| 1 | Daily Standup Simulation | Communication, blocker surfacing, time discipline | 15 min |
| 2 | PR Code Review | Constructive feedback, technical review, decision making | 25 min |
| -- | Debrief + Scoring | Connect it all together | 15 min |

---

## GROUP ASSIGNMENTS

### Group 1 (5 members)
| Role | Participant |
|------|------------|
| A - Senior Backend Engineer | Pappu Tejvardhan |
| B - Frontend Engineer | Pavan Jadhav |
| C - QE Engineer | Aravind Anandhakumar |
| D - Junior Backend Engineer | Honna Reddy G |
| E - Scrum Master | Riya Vengurlekar |

### Group 2 (5 members)
| Role | Participant |
|------|------------|
| A - Senior Backend Engineer | Devanagouda |
| B - Frontend Engineer | Yashas Sawai |
| C - QE Engineer | Dheeraj Naik |
| D - Junior Backend Engineer | Sagar Sajjan |
| E - Scrum Master | Sushmitha G |

### Group 3 (4 members)
| Role | Participant |
|------|------------|
| A - Senior Backend Engineer | Sinchana M K |
| B - Frontend Engineer | Sugesh K G |
| C - QE Engineer | Vedha Mateti |
| D - Junior Backend Engineer | Anirudh M |
| Scrum Master | **Trainer plays this role** |

### Group 4 (5 members)
| Role | Participant |
|------|------------|
| A - Senior Backend Engineer | Rahul S |
| B - Frontend Engineer | Pranav Sourya |
| C - QE Engineer | Ridham Mishra |
| D - Junior Backend Engineer | Sridhar Govindu |
| E - Scrum Master | Eeshaan Bharadwaj |

### Group 5 (4 members)
| Role | Participant |
|------|------------|
| A - Senior Backend Engineer | Dorai Sai Charan |
| B - Frontend Engineer | Surya Kausthub |
| C - QE Engineer | Banashankari Anegundi |
| D - Junior Backend Engineer | Sai Ganesh |
| Scrum Master | **Trainer plays this role** |

### Group 6 (4 members)
| Role | Participant |
|------|------------|
| A - Senior Backend Engineer | Tanuja K C |
| B - Frontend Engineer | Piyush Sidharth |
| C - QE Engineer | Hithesh S A |
| D - Junior Backend Engineer | Dega Dheepakkh |
| Scrum Master | **Trainer plays this role** |

---

## STEP-BY-STEP: EXACTLY WHAT TO DO

---

### STEP 0: SETUP (5 min) -- 15:45

1. Push tables together so each group sits in a circle/cluster
2. Write group numbers on paper tents (Group 1 through 6) and place on tables
3. Call out names from the list above -- people move to their group table
4. Hand each group an envelope with:
   - 1x Scenario Card
   - Role cards (face down, one per person)
   - Do NOT give the code diff yet (that's Round 2)

**Say this:**
> "We are going to do something different for the next hour. No slides. No lecture. You are going to BE an engineering team. Two rounds -- a standup and a code review. I will observe and score each of you individually. This counts."

> "This is NOT a test of your coding ability. This is about how you communicate, how you raise problems, and how you give feedback. Play your role naturally."

---

### STEP 1: ROUND 1 -- DAILY STANDUP (15 min) -- 15:50

**Say this:**
> "Open your envelope. Take ONE role card each. Read it SILENTLY. Do NOT show your card to anyone. You have 2 minutes."

**[Wait 2 minutes. Walk around to make sure everyone has a card.]**

**Say this:**
> "Here is the situation. It is Tuesday, 9:30 AM. Your FoodExpress sustain engineering team is doing its daily standup. Each person gets 90 seconds max. The whole standup must finish in 10 minutes."

> "Scrum Masters -- you keep time. Cut people off politely at 90 seconds. After everyone speaks, summarise the blockers."

> "Groups 3, 5, 6 -- I will come around and play your Scrum Master briefly. Start without me -- Role A speaks first."

> "Ready? Begin."

**[Start your phone timer -- 10 minutes]**

#### What YOU do (walk around and note these):

| Watch For | Scoring |
|-----------|---------|
| Did Role D (junior) admit they're blocked? | This is the KEY moment. If they hide it, note it. |
| Did Role C flag the build dependency? | Should say "I need a build from Dev before I can test FE-95" |
| Did Role B honestly say they're behind? | Should not make excuses, just state the situation |
| Did the Scrum Master keep time? | Should cut people off at 90 sec |
| Did anyone start a deep technical discussion? | RED FLAG -- standups don't solve problems, they surface them |

**[At 10 minutes, call TIME even if groups aren't done]**

#### Debrief (5 min) -- ask the whole class:

**Say this:**
> "Hands up -- how many groups finished within 10 minutes?"

> "Role D players -- stand up. Did you tell your team you were blocked? Was it hard to say 'I'm stuck'? In a real team, a junior hiding a blocker costs the team DAYS. The standup exists to make it safe to say 'I need help.'"

> "One question: what is the difference between a standup and a status meeting? [Pause for answers] A status meeting reports what happened. A standup surfaces what's IN THE WAY. If your standup has no blockers, either your team has no problems -- unlikely -- or people aren't being honest."

---

### STEP 2: ROUND 2 -- PR CODE REVIEW (25 min) -- 16:05

**Say this:**
> "Same groups. New activity. Within your group, pick 3 roles:"
> - **Author** -- you wrote the code, you walk reviewers through it
> - **Reviewer 1 (Logic)** -- you check if the fix is correct
> - **Reviewer 2 (Style & Tests)** -- you check code quality and test coverage
> - If you have 5 people, the remaining 2 observe and take notes

**Distribute the Code Diff printout (one per group).**

**Say this:**
> "Here is a pull request. PR #347. The bug: cart total shows NaN when a coupon is applied and then removed. The Author will walk Reviewers through the fix. Reviewers -- your job is to find issues and give feedback. You have 18 minutes. At the end, you must reach a decision: Approve, Approve with Changes, or Request Changes."

> "One rule: phrase feedback as QUESTIONS, not commands. Say 'Have you considered what happens when...' instead of 'You should have done...'"

> "Go."

#### The Code Diff (what they're reviewing):

```javascript
// File: src/cart/cartUtils.js
// Branch: fix/cart-total-nan-on-coupon-remove
// PR #347

function calculateCartTotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function applyDiscount(total, coupon) {
  if (!coupon || coupon.discountPercent === undefined) {
    return total;
  }
  const discount = total * coupon.discountPercent / 100;
  return total - discount;
}

function getDisplayTotal(cartState) {
  if (!cartState || !cartState.items) {
    return 0;
  }
  const raw = calculateCartTotal(cartState.items);
  const discounted = applyDiscount(raw, cartState.activeCoupon);
  console.log('Cart total calculated:', discounted);    // <-- ISSUE 1
  return discounted;
}

// TODO: add coupon validation                          // <-- ISSUE 3

module.exports = { calculateCartTotal, applyDiscount, getDisplayTotal };
```

#### What Reviewers SHOULD Find (cheat sheet for you):

| # | Issue | Who Should Catch It | Severity |
|---|-------|-------------------|----------|
| 1 | `console.log` left in production code | Reviewer 2 (Style) | BLOCKING -- must remove |
| 2 | No unit tests submitted with the PR | Reviewer 2 (Tests) | BLOCKING -- cannot merge without tests |
| 3 | `// TODO` comment -- incomplete work | Either reviewer | NON-BLOCKING -- ask if follow-up ticket exists |
| 4 | Edge case: `discountPercent = 0` passes the check but is meaningless | Reviewer 1 (Logic) | NON-BLOCKING -- worth discussing |

#### What YOU do (walk around and note these):

| Watch For | Scoring |
|-----------|---------|
| Did they find the console.log? | Every group should catch this |
| Did they ask "where are the tests?" | Critical -- no tests = no merge |
| Was feedback phrased as questions? | "Have you considered..." = good. "This is wrong" = bad |
| Did the Author get defensive? | If yes, let it play 30 sec, then pause and discuss |
| Did they reach a clear decision? | Must end with Approve/Approve with Changes/Request Changes |

**[At 18 minutes, call TIME]**

#### Debrief (7 min) -- ask the whole class:

**Say this:**
> "Show of hands -- how many groups caught the console.log?" [Should be all]

> "How many groups said 'we cannot merge without tests'?" [This is the important one]

> "Authors -- when someone pointed out a problem in YOUR code, what was your first instinct? Did you want to explain why you did it that way? That instinct is natural. But in a code review, the correct response is 'good catch' or 'let me think about that.' Not 'but I did it because...'"

> "Last question: which of these 4 issues would a CI/CD pipeline catch automatically?"
> [Answer: console.log via ESLint rules, missing tests via coverage gates. But the edge case and the TODO? Only a human reviewer catches those. That's why code reviews still matter even with CI/CD.]

---

### STEP 3: FINAL WRAP-UP (5 min) -- 16:30

**Say this:**
> "Step back and look at what you did in the last hour. In the standup, you surfaced a blocker -- a PR waiting for review. In the code review, that review unblocked QE to begin testing. After the merge, CI/CD runs the pipeline."

> "Everything you learned this week is one continuous flow:"
> - **SDLC** -- the stages your code moves through
> - **Jira** -- the board that tracks the work
> - **Git** -- the version control that manages the code
> - **Standup** -- the ceremony that surfaces blockers
> - **PR Review** -- the gate that ensures quality
> - **CI/CD** -- the pipeline that deploys it
> - **DevOps** -- the culture that ties it all together

> "These are not 7 separate topics. They are 7 parts of one machine. Today you operated that machine."

---

## SCORING RUBRIC

### 6 Criteria (5 points each = 30 total per person)

| # | Criteria | 5 (Excellent) | 3 (Good) | 1 (Needs Work) |
|---|----------|--------------|----------|----------------|
| 1 | **Role Understanding** | Played the role exactly as described | Understood role, missed some nuances | Confused about what to do |
| 2 | **Communication Clarity** | Concise, structured, on-point | Got the message across, some rambling | Unclear, off-topic |
| 3 | **Blocker/Risk Surfacing** | Raised issues proactively and clearly | Mentioned issues vaguely | Hid problems or stayed silent |
| 4 | **Constructive Feedback** | Framed as questions, specific, actionable | Correct but blunt or vague | Personal, hostile, or absent |
| 5 | **Team Collaboration** | Active listener, built on others' points | Participated but minimal engagement | Disengaged or talked over others |
| 6 | **Process Awareness** | Clearly understood standup/PR purpose | Followed along adequately | Treated it as a formality |

### Grade Scale

| Score | Grade | Meaning |
|-------|-------|---------|
| 25-30 | A | Excellent -- ready for real team ceremonies |
| 19-24 | B | Good -- understands intent, needs practice |
| 13-18 | C | Developing -- grasps basics, needs coaching |
| < 13  | D | Needs significant improvement |

---

## TROUBLESHOOTING

| Problem | What To Do |
|---------|-----------|
| Group finishes standup in 3 min | That's good! Ask: "Did you surface ALL blockers and dependencies?" If yes, praise. If no, re-run. |
| Nobody catches console.log | Pause everyone. Show the diff on screen. Ask: "What would ESLint catch here?" |
| Author gets defensive | Let it play 30 sec. Then pause. Ask group: "How did that feedback feel? How would you reframe it?" |
| Group treats it as a joke | Walk to that table. Sit down. Say: "I'm your Scrum Master now. Let's restart." Your presence resets the tone. |
| Standup runs over 10 min | Call time. Say: "Your standup just ran 15 minutes. In a real team, people leave at 10. What went wrong?" This IS the learning. |
| Someone refuses to participate | Assign them Observer role. They must write down 3 observations about their group. Score them on the written observations. |

---

## TIMELINE AT A GLANCE

| Time | What | Duration |
|------|------|----------|
| 15:45 | Setup + seating + distribute materials | 5 min |
| 15:50 | Round 1: Standup (10 min play + 5 min debrief) | 15 min |
| 16:05 | Round 2: PR Review (18 min play + 7 min debrief) | 25 min |
| 16:30 | Final wrap-up | 5 min |
| 16:35 | Score tabulation | 10 min |
| 16:45 | Done | -- |

---

## PRINT CHECKLIST

| Item | Copies | Done? |
|------|--------|-------|
| This guide (for yourself) | 1 | [ ] |
| Scenario Card | 6 | [ ] |
| Role Card A (Senior Backend) | 6 | [ ] |
| Role Card B (Frontend) | 6 | [ ] |
| Role Card C (QE) | 6 | [ ] |
| Role Card D (Junior Backend) | 6 | [ ] |
| Role Card E (Scrum Master) | 3 (groups 1,2,4) | [ ] |
| Code Diff printout | 6 | [ ] |
| Scoring sheets (next file) | 6 | [ ] |
| Group number table tents | 6 | [ ] |
