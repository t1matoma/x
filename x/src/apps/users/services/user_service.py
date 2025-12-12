"""
User service - Business logic for users
"""
from typing import Optional, Dict, Any
from django.contrib.auth import authenticate
from django.db import transaction
from src.apps.users.models import User
from src.apps.users.repositories import UserRepository
from src.common.exceptions import ValidationException, NotFoundException


class UserService:
    """
    Service for User business logic
    """

    def __init__(self):
        self.repository = UserRepository()

    def get_all_users(self):
        """Get all users"""
        return self.repository.get_all_users()

    def get_active_users(self):
        """Get all active users"""
        return self.repository.get_active_users()

    def get_user_by_id(self, user_id: int) -> User:
        """Get user by ID"""
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise NotFoundException(f"User with ID {user_id} not found.")
        return user

    def get_user_by_username(self, username: str) -> User:
        """Get user by username"""
        user = self.repository.get_user_by_username(username)
        if not user:
            raise NotFoundException(f"User with username '{username}' not found.")
        return user

    def get_user_by_email(self, email: str) -> User:
        """Get user by email"""
        user = self.repository.get_user_by_email(email)
        if not user:
            raise NotFoundException(f"User with email '{email}' not found.")
        return user

    @transaction.atomic
    def create_user(self, username: str, email: str, password: str, **extra_fields) -> User:
        """Create a new user with validation"""
        # Check if user already exists
        if self.repository.user_exists(username=username):
            raise ValidationException(f"Username '{username}' is already taken.")

        if self.repository.user_exists(email=email):
            raise ValidationException(f"Email '{email}' is already registered.")

        # Create user
        user = self.repository.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )

        # Additional business logic (e.g., send welcome email)
        # self._send_welcome_email(user)

        return user

    @transaction.atomic
    def update_user(self, user_id: int, **fields) -> User:
        """Update user information"""
        user = self.get_user_by_id(user_id)

        # Validate unique fields if being updated
        if 'username' in fields and fields['username'] != user.username:
            if self.repository.user_exists(username=fields['username']):
                raise ValidationException(f"Username '{fields['username']}' is already taken.")

        if 'email' in fields and fields['email'] != user.email:
            if self.repository.user_exists(email=fields['email']):
                raise ValidationException(f"Email '{fields['email']}' is already registered.")

        return self.repository.update_user(user, **fields)

    def delete_user(self, user_id: int) -> None:
        """Soft delete user"""
        user = self.get_user_by_id(user_id)
        self.repository.delete_user(user)

    def search_users(self, query: str):
        """Search users"""
        if not query or len(query) < 2:
            raise ValidationException("Search query must be at least 2 characters long.")
        return self.repository.search_users(query)

    def verify_user(self, user_id: int) -> User:
        """Verify user email"""
        user = self.get_user_by_id(user_id)
        if user.is_verified:
            raise ValidationException("User is already verified.")
        return self.repository.verify_user(user)

    def change_password(self, user: User, old_password: str, new_password: str) -> User:
        """Change user password"""
        # Verify old password
        if not user.check_password(old_password):
            raise ValidationException("Old password is incorrect.")

        # Set new password
        user.set_password(new_password)
        user.save()

        return user

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user"""
        user = authenticate(username=username, password=password)
        if user is None:
            raise ValidationException("Invalid username or password.")

        if not user.is_active:
            raise ValidationException("User account is disabled.")

        return user

    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user statistics"""
        user = self.get_user_by_id(user_id)

        return {
            'total_users': User.objects.count(),
            'verified_users': User.objects.filter(is_verified=True).count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_verified': user.is_verified,
                'is_active': user.is_active,
                'date_joined': user.date_joined,
            }
        }

