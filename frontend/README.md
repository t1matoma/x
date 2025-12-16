# Frontend for Social Media API

A simple HTML/JavaScript frontend for the Django REST API social media application.

## Features

- User registration and login
- JWT token authentication with automatic refresh
- View posts with like counts and comment counts
- Create new posts
- View post details with comments
- Add comments to posts
- Like/unlike posts

## Setup

1. Ensure the Django backend is running on `http://localhost:8000` (default Django development server).
2. Serve the frontend directory on a different port (recommended `8001`) to avoid port conflicts. From PowerShell run:

    ```powershell
    python -m http.server 8001 --directory .;
    # then open http://localhost:8001/index.html in your browser
    ```

3. Register a new account or login with existing credentials.

## API Endpoints Used

- `POST /api/users/auth/login/` - Login
- `POST /api/users/auth/register/` - Register
- `POST /api/users/auth/logout/` - Logout
- `POST /api/users/auth/refresh/` - Refresh access token
- `GET /api/posts/` - List posts
- `POST /api/posts/` - Create post
- `GET /api/posts/{id}/` - Get post details
- `POST /api/posts/{id}/like/` - Like/unlike post
- `GET /api/posts/{id}/comments/` - List comments on post
- `POST /api/posts/{id}/comment/` - Create comment on post

## Notes

- Tokens are stored in localStorage
- The app handles token expiration by attempting to refresh
- CORS must be configured in the Django backend to allow requests from the frontend origin (e.g. `http://localhost:8001`). Add this origin to `CORS_ALLOWED_ORIGINS` in Django settings or enable `CORS_ALLOW_ALL_ORIGINS` for local development.

## Troubleshooting

- If API calls fail with CORS errors, verify Django CORS settings and that the server is running on `http://localhost:8000`.
- If static files fail to load, ensure you served the frontend folder and open the served `index.html` (don't open the file directly in the browser filesystem when testing API calls due to CORS issues).
