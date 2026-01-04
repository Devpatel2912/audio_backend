# Audio Notes Backend

This is the backend API for the Audio Notes application, built with Django and Django REST Framework.

## Features

- **Authentication**: JWT-based authentication (Login, Refresh Token).
- **Folder Management**: Organize your content with a hierarchical folder structure.
- **Audio Management**: Upload, list, and play audio files.
- **PDF Management**: Upload and view PDF files.
- **Note Taking**: 
    - Create timestamped notes for audio files.
    - Create page-specific notes for PDF files.
    - Edit and delete notes.

## Tech Stack

- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Authentication**: `djangorestframework-simplejwt`
- **Database**: PostgreSQL
- **Image Processing**: Pillow
- **Environment Management**: `python-decouple`

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd Backend
    ```

2.  **Create and activate a virtual environment** (Recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Configuration**:
    - Ensure PostgreSQL is installed and running.
    - Create a database named `audionotes_db`.
    - Update the `DATABASES` configuration in `audio_notes_backend/settings.py` if your credentials differ from the defaults:
        ```python
        'USER': 'postgres',
        'PASSWORD': 'system', # Update this to your password
        'HOST': 'localhost',
        ```
    - Alternatively, use environment variables if configured.

5.  **Environment Variables**:
    - Create a `.env` file in the `Backend` directory (next to `manage.py`) to manage sensitive data like `SECRET_KEY` and `DEBUG` status if you prefer not to hardcode them.

6.  **Run Migrations**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7.  **Create a Superuser** (for Admin access):
    ```bash
    python manage.py createsuperuser
    ```

8.  **Run the Server**:
    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```
    The API will be accessible at `http://localhost:8000/api/` (or your machine's IP address).

## API Documentation

For detailed API endpoints, request/response formats, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md) located in this directory.

## Project Structure

- `accounts/`: User authentication and profile management.
- `audios/`: Audio file handling.
- `folders/`: Folder structure logic.
- `notes/`: Note creation and management for both Audio and PDF.
- `pdfs/`: PDF file handling.
- `audio_notes_backend/`: Project settings and main URL configuration.
- `media/`: Directory where uploaded user files (audios, pdfs, images) are stored.

## Common Issues

- **Connection Refused**: Ensure PostgreSQL is running on port 5432.
- **CORS Errors**: If accessing from a frontend on a different port/IP, ensure `CORS_ALLOWED_ORIGINS` in `settings.py` includes your frontend's address. `CORS_ALLOW_ALL_ORIGINS = True` is currently set for development.
