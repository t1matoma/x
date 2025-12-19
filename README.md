# X Clone - Project Documentation

## Project goal

The goal of project X was to develop an educational social network in order to gain practical experience in team-based backend development, REST API design, and the implementation of real-time communication using WebSocket. 

## Features

- **User Authentication**: JWT-based authentication with access and refresh tokens
- **Posts Management**: Create, view, and like posts
- **Comments System**: Add comments to posts
- **Real-time Chat**: WebSocket-based instant messaging

## Tech Stack

### Backend
- **Django 6.0**: Web framework
- **Django REST Framework**: API development
- **Django Channels**: WebSocket support
- **Redis**: Channel layer backend
- **Simple JWT**: Token authentication


### Frontend
- **Vanilla JavaScript**: No framework dependencies


## Architecture

### API Endpoints

#### Authentication
- `POST /api/users/auth/register/` - User registration
- `POST /api/users/auth/login/` - User login
- `POST /api/users/auth/logout/` - User logout

#### Posts
- `GET /api/posts/` - List all posts (paginated)
- `POST /api/posts/` - Create new post
- `GET /api/posts/{id}/` - Get post details
- `POST /api/posts/{id}/like/` - Like/unlike post
- `GET /api/posts/{id}/comments/` - Get post comments
- `POST /api/posts/{id}/comment/` - Add comment to post

#### Chats
- `GET /api/chats/` - List user's chats
- `POST /api/chats/` - Create new chat
- `GET /api/chats/{id}/` - Get chat details
- `GET /api/chats/{id}/messages/` - Get chat messages
- `POST /api/chats/{id}/messages/` - Send message (HTTP fallback)

#### WebSocket
- `ws://localhost:8000/ws/chat/{chat_id}/?token={jwt_token}` - Real-time chat connection

## Setup Instructions

### Prerequisites

- Python 3.10+
- Redis Server

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd x
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install depedencies**
   ```bash
   pip install -r requrements.txt
   ```

4. **Create .env**
   example
   ```init
    # Environment variables template
    # Copy this file to .env and fill in your actual values

    # Django Settings
    SECRET_KEY=your-secret-key-here-generate-new-one
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1

    # Database Settings (PostgreSQL)
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_HOST=localhost
    DB_PORT=5432

    # CORS Settings (if needed)
    CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

    # Email Settings (optional)
    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER=your_email@gmail.com
    EMAIL_HOST_PASSWORD=your_email_password

    # Static and Media Files
    STATIC_URL=/static/
    MEDIA_URL=/media/


   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start Redis server**
   ```bash
   redis-server
   
   # Or with Docker
   docker run -p 6379:6379 redis
   ```

7. **Start Django server**
   ```bash
   python manage.py runserver
   ```

8. **Start frontend server** (in separate terminal)
   ```bash
   # Navigate to project root
   python -m http.server 3000
   ```

9. **Access the application**
    - Frontend: http://localhost:3000/frontend/
    - API: http://localhost:8000/api/
    - Admin: http://localhost:8000/admin/



## Security Considerations

- **JWT Tokens**: Short-lived access tokens (5 min) with refresh mechanism
- **WebSocket Authentication**: Token verification on connection
- **Chat Membership**: Users can only access chats they're members of
- **CORS**: Restrictive CORS policy for production
- **Input Validation**: All inputs validated on backend
- **SQL Injection**: Protection via Django ORM

## License

This project is for educational purposes.