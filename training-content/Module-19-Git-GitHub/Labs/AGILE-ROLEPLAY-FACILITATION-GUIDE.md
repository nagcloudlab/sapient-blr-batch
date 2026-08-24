# Agile Role Play -- Trainer Facilitation Guide

**Date:** Fri Aug 21, 2026 | **Day 18** | **Duration:** 75 min (including scoring)
**Context:** Covers Infra, SDLC, Jira/Confluence, DevOps, Git, CI/CD
**Batch:** 27 participants | **Groups:** 6 (4-5 per group)

---

## QUICK OVERVIEW (Read this first)

You are running TWO rounds:
1. **Round 1 -- Daily Standup Simulation** (15 min) -- tests communication, blocker surfacing
2. **Round 2 -- PR Code Review** (25 min) -- tests constructive feedback, technical review skills

Then a **debrief + scoring** (20 min). You observe all groups simultaneously.

---

## GROUP ASSIGNMENTS (6 Groups)

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

### Group 3 (4 members -- Trainer floats as Scrum Master)
| Role | Participant |
|------|------------|
| A - Senior Backend Engineer | Sinchana M K |
| B - Frontend Engineer | Sugesh K G |
| C - QE Engineer | Vedha Mateti |
| D - Junior Backend Engineer | Anirudh M |

### Group 4 (5 members)
| Role | Participant |
|------|------------|
| A - Senior Backend Engineer | Rahul S |
| B - Frontend Engineer | Pranav Sourya |
| C - QE Engineer | Ridham Mishra |
| D - Junior Backend Engineer | Sridhar Govindu |
| E - Scrum Master | Eeshaan Bharadwaj |

### Group 5 (4 members -- Trainer floats as Scrum Master)
| Role | Participant |
|------|------------|
| A - Senior Backend Engineer | Dorai Sai Charan |
| B - Frontend Engineer | Surya Kausthub |
| C - QE Engineer | Banashankari Anegundi |
| D - Junior Backend Engineer | Sai Ganesh |

### Group 6 (4 members -- Trainer floats as Scrum Master)
| Role | Participant |
|------|------------|
| A - Senior Backend Engineer | Tanuja K C |
| B - Frontend Engineer | Piyush Sidharth |
| C - QE Engineer | Hithesh S A |
| D - Junior Backend Engineer | Dega Dheepakkh |

> **Tip:** Groups 3, 5, 6 have 4 members. For these groups, briefly play the Scrum Master yourself to model the correct behaviour, OR ask one member to double up.

---

## STEP-BY-STEP FACILITATION

### BEFORE YOU START (5 min) -- 15:45 to 15:50

1. **Rearrange seating** -- push tables together so each group sits in a circle
2. **Distribute printed materials** to each group:
   - 1x Scenario Card (the FoodExpress context paragraph)
   - Role cards (cut into individual slips, face down)
   - 1x Code Diff printout (keep aside for Round 2)
3. **Set expectations** (say this aloud):

> "This is NOT a test of your JavaScript or technical knowledge. This is about practising HOW you communicate in an engineering team. There are no trick questions. Play your role naturally. I will observe and score each group."

> "Two rounds. Round 1 is a standup -- 10 minutes. Round 2 is a code review -- 18 minutes. After each round we debrief as a class."

---

### ROUND 1: DAILY STANDUP (15 min) -- 15:50 to 16:05

#### Your Script (say this):
> "Read your role card silently. You have 2 minutes. Do NOT share your card with others -- that's the point. In a real standup, only YOU know your situation."

**[2 min silent reading]**

> "It is Tuesday, 9:30 AM. Your FoodExpress sustain team standup begins NOW. Scrum Masters -- start the timer. Each person gets 90 seconds max. Go."

#### What YOU Do During Round 1:
- Walk between groups with your scoring sheet
- **Listen for these specific things** (this is what you score):

| What to Watch | Good Sign | Red Flag |
|--------------|-----------|----------|
| Blocker surfacing | Role D admits they're stuck | Role D hides the blocker |
| Time discipline | Each person under 90 sec | Someone rambles for 3+ min |
| Standup vs status meeting | Short updates, blockers flagged | Deep technical discussions start |
| Scrum Master behaviour | Cuts people off politely, notes blockers | Lets it run wild, or dominates |
| Dependency flagging | Role C mentions build dependency | Role C says nothing about it |

**[10 min standup]**

#### Round 1 Debrief (5 min) -- ask the whole class:
1. "How many groups finished within 10 minutes?" (show of hands)
2. "Role D players -- did you raise your blocker? Was it hard? Why?"
3. "What is the ONE difference between a standup and a status meeting?" (Answer: standup surfaces problems, status meeting reports progress)

---

### ROUND 2: PR CODE REVIEW (25 min) -- 16:05 to 16:30

#### Your Script:
> "New round. Same groups. Now distribute yourselves into 3 roles: Author, Reviewer 1 (Logic), Reviewer 2 (Style/Tests). If you have 5 people, remaining 2 observe and take notes."

> "Here is a PR diff. The Author will walk reviewers through the code. Reviewers -- your job is to find problems and give feedback constructively. You have 18 minutes."

**Distribute the code diff printout (one per group).**

#### What YOU Do During Round 2:
- Walk between groups with your scoring sheet
- **Listen for these specific things:**

| What to Watch | Good Sign | Red Flag |
|--------------|-----------|----------|
| console.log found | Reviewer catches it, asks to remove | Nobody notices |
| Missing tests raised | "Where are the unit tests?" | PR approved without test discussion |
| Feedback tone | "Have you considered..." / "What happens when..." | "You should have..." / "This is wrong" |
| Edge case (0% discount) | Raised as a question | Ignored |
| TODO comment discussed | "Will this be a follow-up ticket?" | Ignored |
| Decision reached | Clear "approve with changes" or "request changes" | No decision, just chatting |

**[18 min code review]**

#### Round 2 Debrief (7 min) -- ask the whole class:
1. "How many groups caught the console.log?" (should be all)
2. "How many groups asked about missing tests?" (critical)
3. "Authors -- when someone pointed out an issue, how did it feel? Did you get defensive?"
4. "What is a blocking comment vs a non-blocking comment?" (Answer: blocking = must fix before merge; non-blocking = nice to have, can be a follow-up)
5. "In a CI/CD pipeline, which of these issues would be caught automatically?" (Answer: console.log via lint rules, missing tests via coverage gates)

---

### FINAL CONNECTION (say this) -- 16:30 to 16:35

> "Notice how these two activities connect. In the standup, your team found that a PR was waiting for review. In the PR review, that review unblocked QE to start testing. This is how a healthy DevOps team works every single day -- standup surfaces the work, reviews unblock the flow, CI/CD catches the rest."

> "Everything you learned this week -- SDLC phases, Jira boards, Git branching, CI/CD pipelines -- these are not separate topics. They are one continuous flow. The standup is your Jira board come alive. The PR is your Git workflow in action. The pipeline runs after the merge."

---

## SCORING RUBRIC

### Individual Score Card (per participant)

| # | Criteria | Max | How to Score |
|---|----------|-----|-------------|
| 1 | **Role Understanding** -- Did they play their assigned role correctly? | 5 | 5=nailed it, 3=partial, 1=confused about role |
| 2 | **Communication Clarity** -- Were updates/feedback concise and clear? | 5 | 5=crisp and structured, 3=rambling but got there, 1=unclear |
| 3 | **Blocker/Risk Surfacing** -- Did they raise issues proactively? | 5 | 5=flagged early and clearly, 3=mentioned vaguely, 0=hid it |
| 4 | **Constructive Feedback** -- Was feedback professional and actionable? | 5 | 5=framed as questions, specific, 3=correct but blunt, 1=personal/hostile |
| 5 | **Team Collaboration** -- Did they listen, respond, build on others? | 5 | 5=active listener, engaged, 3=participated minimally, 1=disengaged |
| 6 | **Process Awareness** -- Understood standup/PR review purpose? | 5 | 5=demonstrated clearly, 3=followed along, 1=treated it as a formality |
| **Total** | | **30** | |

### Grading Scale

| Score | Grade | Meaning |
|-------|-------|---------|
| 25-30 | A | Excellent -- ready for team ceremonies |
| 19-24 | B | Good -- understands the intent, needs practice |
| 13-18 | C | Developing -- grasps basics, needs coaching |
| < 13 | D | Needs significant improvement |

---

## PRINTABLE SCORING SHEET

Use one sheet per group. Circle scores as you observe.

```
GROUP: ___  |  ROUND 1 (Standup)  |  ROUND 2 (PR Review)

Participant Name          | Role | R1  R2  R3  R4  R5  R6 | TOTAL /30
--------------------------|------|-------------------------|----------
_________________________ | ____ | __  __  __  __  __  __ | ____
_________________________ | ____ | __  __  __  __  __  __ | ____
_________________________ | ____ | __  __  __  __  __  __ | ____
_________________________ | ____ | __  __  __  __  __  __ | ____
_________________________ | ____ | __  __  __  __  __  __ | ____

R1=Role Understanding  R2=Communication  R3=Blocker Surfacing
R4=Constructive Feedback  R5=Collaboration  R6=Process Awareness

Group Observations:
_______________________________________________________________
_______________________________________________________________
_______________________________________________________________
```

---

## MATERIALS CHECKLIST (Print Before Session)

| Item | Copies | Status |
|------|--------|--------|
| Scenario Card (FoodExpress context paragraph) | 6 (one per group) | [ ] |
| Role Card A (Senior Backend Engineer) | 6 copies | [ ] |
| Role Card B (Frontend Engineer) | 6 copies | [ ] |
| Role Card C (QE Engineer) | 6 copies | [ ] |
| Role Card D (Junior Backend Engineer) | 6 copies | [ ] |
| Role Card E (Scrum Master) | 4 copies (groups 1,2,4 + spare) | [ ] |
| Code Diff (PR #347) | 6 copies | [ ] |
| Scoring Sheets (blank, from above) | 6 copies | [ ] |
| Timer (phone/watch) | 1 | [ ] |

> **All role cards and the code diff are in:** `training-content/Module-19-Git-GitHub/Labs/role-play.md`
> Print that file and cut the role cards along the dotted lines.

---

## IF THINGS GO WRONG

| Problem | What To Do |
|---------|-----------|
| A group finishes Round 1 in 3 minutes | Good -- that means they were concise. Ask them: "Did you surface ALL blockers?" If yes, praise them. If no, ask them to re-run. |
| Nobody catches the console.log | Pause all groups. Show the diff on screen. Ask: "What would your CI lint rules catch here?" |
| Author gets defensive in Round 2 | Let it play out for 30 seconds, then pause that group. Ask: "How did that feel? How would you reframe that feedback?" |
| A group turns it into a joke | Walk to that group. Sit down. Say: "I'm your Scrum Master now. Let's restart." Your presence will reset the tone. |
| Round 1 runs over 10 min | Call time firmly. Say: "Your standup just ran 15 minutes. In a real team, people walk away at 10. What went wrong?" -- this itself is a learning moment. |

---

## TIMELINE SUMMARY

| Time | Activity | Duration |
|------|----------|----------|
| 15:45 | Setup, seating, distribute materials | 5 min |
| 15:50 | Round 1: Standup (10 min play + 5 min debrief) | 15 min |
| 16:05 | Round 2: PR Review (18 min play + 7 min debrief) | 25 min |
| 16:30 | Final connection + wrap-up | 5 min |
| 16:35 | Score tabulation + individual feedback | 10 min |
| 16:45 | Submit scores | 5 min |
| **Total** | | **60-70 min** |
