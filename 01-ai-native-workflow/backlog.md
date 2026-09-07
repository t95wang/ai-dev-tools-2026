# Chore Claim System Backlog

## 1. Create the Chore Model

**Goal:** Store chores and their lifecycle information in the database.

**Acceptance criteria:**

- A chore has a title, description, due date, and status.
- Claim details include optional `claimed_by` and `claimed_at` fields.
- Completion details include optional `completed_by` and `completed_at` fields.
- New chores default to `Unclaimed`.
- A migration creates the required database table.

## 2. Add Chore Creation

**Goal:** Allow a household member to create a chore.

**Acceptance criteria:**

- A page provides fields for title, description, and due date.
- Valid submissions create an `Unclaimed` chore.
- Invalid submissions display useful validation errors.
- Successful submissions return the user to the chore list.

## 3. Add the Chore List

**Goal:** Display household chores and make available chores easy to identify.

**Acceptance criteria:**

- The list displays each chore's title, description, due date, and status.
- Unclaimed chores are clearly shown as available to claim.
- The page provides access to the chore creation page.

## 4. Add Chore Claiming

**Goal:** Allow an unclaimed chore to be claimed once.

**Acceptance criteria:**

- A user can provide their name when claiming an unclaimed chore.
- Claiming records `claimed_by` and the current time in `claimed_at`.
- The status changes from `Unclaimed` to `Claimed`.
- A chore that is already claimed or completed cannot be claimed again.

## 5. Add Chore Completion

**Goal:** Allow a claimed chore to be marked as completed.

**Acceptance criteria:**

- A user can provide their name when completing a claimed chore.
- Completion records `completed_by` and the current time in `completed_at`.
- The status changes from `Claimed` to `Completed`.
- An unclaimed or completed chore cannot be completed.

## 6. Test the Chore Lifecycle

**Goal:** Verify the complete version 1 workflow and its transition rules.

**Acceptance criteria:**

- Tests cover creating and listing a chore.
- Tests cover the `Unclaimed -> Claimed -> Completed` lifecycle.
- Tests confirm repeated claims and invalid completions are rejected.
- `python manage.py check` and `python manage.py test` complete successfully.
