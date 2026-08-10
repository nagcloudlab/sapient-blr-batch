# Git Hands-On Exercises

## Exercise 1: Repository Setup

### Steps
1. Create a new directory called `foodexpress-practice`
   ```bash
   mkdir foodexpress-practice
   cd foodexpress-practice
   ```

2. Initialize a Git repository
   ```bash
   TODO: What command initializes a new Git repo?
   ```

3. Configure your name and email (local to this repo)
   ```bash
   TODO: Set your Git username
   TODO: Set your Git email
   ```

4. Create an initial file and make your first commit
   ```bash
   echo "# FoodExpress Practice" > README.md
   TODO: Stage the file
   TODO: Commit with message "Initial commit"
   ```

5. Verify your commit
   ```bash
   TODO: What command shows the commit history?
   ```

---

## Exercise 2: Branching and Merging

### Steps
1. Create and switch to a new branch called `feature/add-menu`
   ```bash
   TODO: Create and switch to the new branch in one command
   ```

2. Create a menu file
   ```bash
   echo "Butter Chicken - Rs. 350" > menu.txt
   echo "Paneer Tikka - Rs. 280" >> menu.txt
   TODO: Stage and commit with message "feat: add menu items"
   ```

3. Switch back to main/master branch
   ```bash
   TODO: Switch to main branch
   ```

4. Merge the feature branch
   ```bash
   TODO: Merge feature/add-menu into main
   ```

5. Delete the merged branch
   ```bash
   TODO: Delete the feature/add-menu branch
   ```

---

## Exercise 3: Creating a Merge Conflict

### Steps
1. Create a branch `feature/update-prices`
   ```bash
   TODO: Create and switch to branch
   ```

2. Edit menu.txt - change Butter Chicken price to Rs. 400
   ```bash
   # Edit the file to change the price
   TODO: Stage and commit with message "feat: increase butter chicken price"
   ```

3. Switch back to main and create another branch `feature/menu-discount`
   ```bash
   TODO: Switch to main
   TODO: Create and switch to feature/menu-discount
   ```

4. Edit menu.txt - change Butter Chicken price to Rs. 300 (discount)
   ```bash
   # Edit the file to change the price differently
   TODO: Stage and commit with message "feat: apply discount to butter chicken"
   ```

5. Merge feature/update-prices into main first
   ```bash
   TODO: Switch to main
   TODO: Merge feature/update-prices
   ```

6. Now try to merge feature/menu-discount
   ```bash
   TODO: Merge feature/menu-discount
   # This should cause a CONFLICT!
   ```

---

## Exercise 4: Resolving the Merge Conflict

### Steps
1. Check the status to see conflicted files
   ```bash
   TODO: What command shows the current status?
   ```

2. Open menu.txt and look for conflict markers
   ```
   <<<<<<< HEAD
   Butter Chicken - Rs. 400
   =======
   Butter Chicken - Rs. 300
   >>>>>>> feature/menu-discount
   ```

3. Resolve the conflict by choosing the correct price (Rs. 350 - original)
   ```bash
   # Edit menu.txt to remove conflict markers and set the correct price
   TODO: Edit the file
   ```

4. Mark the conflict as resolved and complete the merge
   ```bash
   TODO: Stage the resolved file
   TODO: Complete the merge commit
   ```

5. Verify the merge
   ```bash
   TODO: Check the log with a graph view
   ```

---

## Exercise 5: Git Stash

### Steps
1. Start working on a new feature
   ```bash
   echo "Biryani - Rs. 320" >> menu.txt
   ```

2. Suddenly you need to fix a bug on main! Stash your work
   ```bash
   TODO: Stash your changes with a message
   ```

3. Fix the bug (simulate)
   ```bash
   echo "# Bug fix applied" >> README.md
   TODO: Stage and commit the bug fix
   ```

4. Bring back your stashed changes
   ```bash
   TODO: Apply the stash
   ```

5. Verify stashed changes are restored
   ```bash
   TODO: Check the diff to see your changes
   ```

---

## Exercise 6: Interactive Git Log

### Steps
Try these different log formats:

```bash
# One-line log
TODO: Show log with --oneline flag

# Graph view
TODO: Show log with --graph --oneline --all flags

# Last 5 commits
TODO: Show only the last 5 commits

# Commits by a specific author
TODO: Show commits filtered by your name
```

---

## Bonus: .gitignore Exercise

1. Create files that should be ignored:
   ```bash
   mkdir node_modules
   echo "secret" > .env
   echo "error log" > app.log
   ```

2. Create a proper .gitignore (refer to the .gitignore file in this lab)

3. Verify the files are ignored:
   ```bash
   TODO: Check which files are being tracked/ignored
   ```
