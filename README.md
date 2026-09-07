# Chore Claim System

A simple web application for managing shared household chores. Household members can create, view, claim, and complete chores through a straightforward status workflow.

## Tech Stack

- Python 3.11
- Django 4.2
- SQLite

## Core Scope

- Create chores with a title, description, due date, and status.
- View chores and identify those available to claim.
- Claim an unclaimed chore, recording `claimed_by` and `claimed_at`.
- Complete a claimed chore, recording `completed_by` and `completed_at`.
- Follow the status flow: `Unclaimed -> Claimed -> Completed`.
- No authentication or permissions in version 1.

See [_docs/plan.md](_docs/plan.md) for the complete specification.

## Setup and Run

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Open <http://127.0.0.1:8000/> in a browser.
