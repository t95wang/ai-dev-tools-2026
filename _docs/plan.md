# Chore Claim System

## Overview

The Chore Claim System is a Django web application for managing shared household chores. Version 1 provides a simple workflow without authentication or permissions.

## Core Features

### Create Chores

Any household member can create a chore with:

- Title
- Description
- Due date
- Status

New chores start with the status `Unclaimed`.

### View Available Chores

Users can view household chores and see each chore's title, description, due date, and current status. Unclaimed chores must be clearly identifiable as available.

### Claim Chores

An unclaimed chore can be claimed by recording:

- `claimed_by`
- `claimed_at`

Claiming changes the status from `Unclaimed` to `Claimed`. A claimed chore cannot be claimed again.

### Complete Chores

A claimed chore can be completed by recording:

- `completed_by`
- `completed_at`

Completing changes the status from `Claimed` to `Completed`.

## Status Workflow

```text
Unclaimed -> Claimed -> Completed
```

Only these forward transitions are valid in version 1.

## Technical Direction

- Use Django for the application.
- Create a Django project and a chore-management app.
- Store chores and lifecycle metadata in a database model.
- Implement views and templates for creating, listing, claiming, and completing chores.
- Add tests covering the main chore lifecycle and invalid transitions.

## Out of Scope for Version 1

- Authentication
- User roles or permissions
- Automatic chore rotation
- Recurring chores
- Points or rewards
- Notifications

## Success Criteria

Version 1 is complete when a user can create and view chores, claim an unclaimed chore, complete a claimed chore, and see the correct status throughout the workflow.
