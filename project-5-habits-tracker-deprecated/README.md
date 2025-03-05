# Habit Tracker

## Overview

Habit Tracker is a Django-based web application designed to help users manage and track their daily habits. This application allows users to add, list, edit, and remove habits while also providing features for daily tracking and analysis of habit adherence.

## Project Setup

The project uses Django as its primary framework with SQLite as the default database for development. The setup involves creating a Django project with a single app called `tracker` to handle the habit-related functionality.

### Directory Structure

The project has the following key directories and files:

- `habits_tracker/` - The main project directory containing settings and configurations.
  - `settings.py` - Configuration settings for the Django project, including installed apps, database configurations, and more.
  - `urls.py` - The URL declarations for the Django project; this is a "table of contents" for your Django-powered site.
- `tracker/` - The Django app that contains the logic and database models for the Habit Tracker.
  - `models.py` - Defines the data models (database schema).
  - `views.py` - Handles the request-response cycle for your web application.
  - `admin.py` - Configures the admin interface, which Django provides by default.
- `manage.py` - A command-line utility that lets you interact with this Django project.
- `db.sqlite3` - The SQLite database file containing all the data for the application.

### Technology Stack

- **Backend Framework**: Django
- **Database**: SQLite (default for Django)
- **Frontend**: (To be defined; typically involves HTML, CSS, JavaScript, and Django Templates)

## Local Development

### Prerequisites

- Python 3
- pip (Python package installer)
- Virtual environment (recommended for Python package management)

### Setup Instructions

1. **Create and Activate Virtual Environment (optional but recommended)**
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Required Python Packages**
   ```
   pip install -r requirements.txt
   ```

3. **Run Migrations**
   ```
   python manage.py migrate
   ```

4. **Start the Development Server**
   ```
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000` in your web browser to view the application.

### Configurations

- **Django Settings**: Configure Django settings such as `DEBUG`, `ALLOWED_HOSTS`, and database configurations in `habits_tracker/settings.py`.
