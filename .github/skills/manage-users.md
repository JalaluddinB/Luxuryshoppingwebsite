# User Role Management Skill

This skill explains how to manage user access and roles within the application (AW-05).

## Overview
The platform uses Role-Based Access Control (RBAC) to differentiate between standard customers and administrators.

## Roles
- **Customer**: Default role. Can browse, chat with Lux, and place orders.
- **Admin**: Has `is_admin=True`. Can access `/admin`, manage inventory, and process orders.

## Management Tasks

### 1. Creating an Admin
- **Current Method**: Direct database modification.
- **Steps**:
  1. Open python shell: `./venv/bin/python3` -> `from app import app, db, User` -> `app.app_context().push()`.
  2. Find user: `u = User.query.filter_by(username='target_user').first()`.
  3. Promote: `u.is_admin = True` -> `db.session.commit()`.

### 2. Checking Access
- **Code**: Routes use `if not user.is_admin: return redirect(...)` check.
- **UI**: Admin Dashboard link covers logic to strict access.

### 3. Future Improvements
- Add an Admin User Management UI (currently marked as ⚠️ Partially Implemented in PRD).

## Relevant Files
- `app.py` (`User` model, admin route decorators)
- `templates/base.html` (Conditional rendering of "Admin Panel" link)
