from django.db.models import Q, QuerySet
from typing import Optional
from src.apps.users.models import User

class UserRepository:
    @staticmethod
    def get_all_users() -> QuerySet[User]:
        return User.objects.all()
    @staticmethod
    def get_active_users() -> QuerySet[User]:
        return User.objects.filter(is_active=True
                                   )
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    @staticmethod
    def user_exists(username: str = None, email: str = None) -> bool:
        query = Q()
        if username:
            query |= Q(username=username)
        if email:
            query |= Q(email=email)
        return User.objects.filter(query).exists()


    @staticmethod
    def create_user(username: str, email: str, password: str, **extra_fields) -> User:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields
        )
        return user

    @staticmethod
    def update_user(user: User, **fields) -> User:
        for field, value in fields.items():
            setattr(user, field, value)
        user.save()
        return user

    @staticmethod
    def delete_user(user: User) -> None:
        user.is_active = False
        user.save()

    @staticmethod
    def search_users(query: str) -> QuerySet[User]:
        return User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))
    @staticmethod
    def verify_user(user: User) -> User:
        user.is_verified = True
        user.save()
        return user

    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[User]:
        return User.objects.filter(username=username, password=password).first()

    @staticmethod
    def change_password(user: User, new_password: str) -> None:
        user.set_password(new_password)
        user.save()
