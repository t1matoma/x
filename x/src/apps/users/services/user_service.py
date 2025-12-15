from typing import Optional, Dict, Any
from django.contrib.auth import authenticate
from django.db import transaction
from src.apps.users.models import User
from src.apps.users.repositories import UserRepository
from src.common.exceptions import ValidationException, NotFoundException


class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_all_users(self):
        return self.repository.get_all_users()

    def get_active_users(self):
        return self.repository.get_active_users()

    def get_user_by_id(self, user_id: int) -> User:
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise NotFoundException(f"User with ID {user_id} not found.")
        return user

    def get_user_by_username(self, username: str) -> User:
        user = self.repository.get_user_by_username(username)
        if not user:
            raise NotFoundException(f"User with username '{username}' not found.")
        return user

    def get_user_by_email(self, email: str) -> User:
        user = self.repository.get_user_by_email(email)
        if not user:
            raise NotFoundException(f"User with email '{email}' not found.")
        return user

    @transaction.atomic
    def create_user(self, username: str, email: str, password: str, **extra_fields) -> User:
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
        return user

    @transaction.atomic
    def update_user(self, user_id: int, **fields) -> User:
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
        if not query or len(query) < 2:
            raise ValidationException("Search query must be at least 2 characters long.")
        return self.repository.search_users(query)

    def verify_user(self, user_id: int) -> User:
        user = self.get_user_by_id(user_id)
        if user.is_verified:
            raise ValidationException("User is already verified.")
        return self.repository.verify_user(user)

    def change_password(self, user_id: int, old_password: str, new_password: str) -> User:
        """Change user password"""
        user = self.get_user_by_id(user_id)
        if not user.check_password(old_password):
            raise ValidationException("Old password is incorrect.")

        user.set_password(new_password)
        user.save()
        return user

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user is None:
            raise ValidationException("Invalid username or password.")
        user = User.objects.get(pk=authenticated_user.pk)

        if not user.is_active:
            raise ValidationException("User account is disabled.")

        return user


    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
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

