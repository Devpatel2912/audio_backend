# Audio Notes Backend API Documentation

## Base URL
```
http://127.0.0.1:8000/api
```

## Database Table Names
When checking the database in pgAdmin, note that Django creates tables with the format `appname_modelname`:
- User table: `accounts_user` (NOT `user` or `users`)
- Folder table: `folders_folder`
- Audio table: `audios_audio`
- Note table: `notes_note`

## Authentication
All endpoints except `/api/auth/register/` and `/api/auth/login/` require JWT authentication.

Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

## 1. Authentication APIs

### 1.1 Register User
**Endpoint:** `POST /api/auth/register/`

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Error Response (400 Bad Request):**
```json
{
  "password": ["Password fields didn't match."]
}
```

---

### 1.2 Login
**Endpoint:** `POST /api/auth/login/`

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Error Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials"
}
```

---

### 1.3 Refresh Token
**Endpoint:** `POST /api/auth/token/refresh/`

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### 1.4 Get User Profile
**Endpoint:** `GET /api/auth/profile/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## 2. Folder APIs

### 2.1 List Folders (Root Level)
**Endpoint:** `GET /api/folders/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Work",
      "parent": null,
      "user": 1,
      "created_at": "2024-01-15T10:35:00Z",
      "children": []
    },
    {
      "id": 2,
      "name": "Personal",
      "parent": null,
      "user": 1,
      "created_at": "2024-01-15T10:36:00Z",
      "children": []
    }
  ]
}
```

---

### 2.2 Create Folder
**Endpoint:** `POST /api/folders/create/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Work",
  "parent": null
}
```

**Request Body (Sub-folder):**
```json
{
  "name": "Projects",
  "parent": 1
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Work",
  "parent": null,
  "user": 1,
  "created_at": "2024-01-15T10:35:00Z"
}
```

---

### 2.3 Get Folder Tree (Recursive)
**Endpoint:** `GET /api/folders/tree/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Work",
    "parent": null,
    "user": 1,
    "created_at": "2024-01-15T10:35:00Z",
    "children": [
      {
        "id": 3,
        "name": "Projects",
        "parent": 1,
        "user": 1,
        "created_at": "2024-01-15T10:40:00Z",
        "children": []
      }
    ]
  },
  {
    "id": 2,
    "name": "Personal",
    "parent": null,
    "user": 1,
    "created_at": "2024-01-15T10:36:00Z",
    "children": []
  }
]
```

---

### 2.4 Get Folder Detail
**Endpoint:** `GET /api/folders/<id>/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Work",
  "parent": null,
  "user": 1,
  "created_at": "2024-01-15T10:35:00Z",
  "children": [
    {
      "id": 3,
      "name": "Projects",
      "parent": 1,
      "user": 1,
      "created_at": "2024-01-15T10:40:00Z",
      "children": []
    }
  ]
}
```

---

### 2.5 Update Folder
**Endpoint:** `PUT /api/folders/<id>/` or `PATCH /api/folders/<id>/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Work Updated"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Work Updated",
  "parent": null,
  "user": 1,
  "created_at": "2024-01-15T10:35:00Z",
  "children": []
}
```

---

### 2.6 Delete Folder
**Endpoint:** `DELETE /api/folders/<id>/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (204 No Content)**

---

## 3. Audio APIs

### 3.1 List Audios
**Endpoint:** `GET /api/audios/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `folder` (optional): Filter by folder ID

**Example:** `GET /api/audios/?folder=1`

**Response (200 OK):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Meeting Recording",
      "audio_file": "http://127.0.0.1:8000/media/audio/1/recording.mp3",
      "duration": 3600.5,
      "last_played_position": 1200.0,
      "folder": 1,
      "user": 1,
      "created_at": "2024-01-15T11:00:00Z"
    },
    {
      "id": 2,
      "title": "Lecture Notes",
      "audio_file": "http://127.0.0.1:8000/media/audio/1/lecture.mp3",
      "duration": 7200.0,
      "last_played_position": 0.0,
      "folder": null,
      "user": 1,
      "created_at": "2024-01-15T11:30:00Z"
    }
  ]
}
```

---

### 3.2 Upload Audio
**Endpoint:** `POST /api/audios/upload/`

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
```
title: "Meeting Recording"
audio_file: <file>
duration: 3600.5
folder: 1 (optional)
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Meeting Recording",
  "audio_file": "http://127.0.0.1:8000/media/audio/1/recording.mp3",
  "duration": 3600.5,
  "last_played_position": 0.0,
  "folder": 1,
  "user": 1,
  "created_at": "2024-01-15T11:00:00Z"
}
```

---

### 3.3 Get Audio Detail
**Endpoint:** `GET /api/audios/<id>/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Meeting Recording",
  "audio_file": "http://127.0.0.1:8000/media/audio/1/recording.mp3",
  "duration": 3600.5,
  "last_played_position": 1200.0,
  "folder": 1,
  "user": 1,
  "created_at": "2024-01-15T11:00:00Z"
}
```

---

### 3.4 Update Audio
**Endpoint:** `PUT /api/audios/<id>/` or `PATCH /api/audios/<id>/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "title": "Updated Title",
  "duration": 3800.0,
  "folder": 2
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Updated Title",
  "audio_file": "http://127.0.0.1:8000/media/audio/1/recording.mp3",
  "duration": 3800.0,
  "last_played_position": 1200.0,
  "folder": 2,
  "user": 1,
  "created_at": "2024-01-15T11:00:00Z"
}
```

---

### 3.5 Update Playback Position
**Endpoint:** `PATCH /api/audios/<id>/position/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "last_played_position": 1500.5
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Meeting Recording",
  "audio_file": "http://127.0.0.1:8000/media/audio/1/recording.mp3",
  "duration": 3600.5,
  "last_played_position": 1500.5,
  "folder": 1,
  "user": 1,
  "created_at": "2024-01-15T11:00:00Z"
}
```

---

### 3.6 Delete Audio
**Endpoint:** `DELETE /api/audios/<id>/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (204 No Content)**

---

## 4. Notes APIs

### 4.1 Create Note
**Endpoint:** `POST /api/notes/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "audio": 1,
  "note_text": "Important point about the project timeline",
  "audio_timestamp": 1250.5
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "audio": 1,
  "note_text": "Important point about the project timeline",
  "audio_timestamp": 1250.5,
  "created_at": "2024-01-15T12:00:00Z"
}
```

---

### 4.2 List Notes by Audio
**Endpoint:** `GET /api/notes/audio/<audio_id>/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "audio": 1,
    "note_text": "Important point about the project timeline",
    "audio_timestamp": 1250.5,
    "created_at": "2024-01-15T12:00:00Z"
  },
  {
    "id": 2,
    "audio": 1,
    "note_text": "Action item: Follow up with team",
    "audio_timestamp": 2400.0,
    "created_at": "2024-01-15T12:05:00Z"
  },
  {
    "id": 3,
    "audio": 1,
    "note_text": "Budget discussion",
    "audio_timestamp": 3200.0,
    "created_at": "2024-01-15T12:10:00Z"
  }
]
```

**Note:** Notes are ordered by `audio_timestamp` (ascending)

---

### 4.3 Get Note Detail
**Endpoint:** `GET /api/notes/<id>/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "audio": 1,
  "note_text": "Important point about the project timeline",
  "audio_timestamp": 1250.5,
  "created_at": "2024-01-15T12:00:00Z"
}
```

---

### 4.4 Update Note
**Endpoint:** `PUT /api/notes/<id>/` or `PATCH /api/notes/<id>/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "note_text": "Updated note text",
  "audio_timestamp": 1300.0
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "audio": 1,
  "note_text": "Updated note text",
  "audio_timestamp": 1300.0,
  "created_at": "2024-01-15T12:00:00Z"
}
```

---

### 4.5 Delete Note
**Endpoint:** `DELETE /api/notes/<id>/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (204 No Content)**

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "A server error occurred."
}
```

---

## Example cURL Commands

### Register
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### Create Folder
```bash
curl -X POST http://127.0.0.1:8000/api/folders/create/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Work",
    "parent": null
  }'
```

### Upload Audio
```bash
curl -X POST http://127.0.0.1:8000/api/audios/upload/ \
  -H "Authorization: Bearer <access_token>" \
  -F "title=Meeting Recording" \
  -F "audio_file=@/path/to/recording.mp3" \
  -F "duration=3600.5" \
  -F "folder=1"
```

### Create Note
```bash
curl -X POST http://127.0.0.1:8000/api/notes/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "audio": 1,
    "note_text": "Important point",
    "audio_timestamp": 1250.5
  }'
```

---

## Pagination

List endpoints support pagination with the following query parameters:
- `page`: Page number (default: 1)
- Page size: 20 items per page

**Pagination Response:**
```json
{
  "count": 50,
  "next": "http://127.0.0.1:8000/api/audios/?page=2",
  "previous": null,
  "results": [...]
}
```

