from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password


class CustomUserManager(UserManager):
    """Класс отвечающий за создание юзера"""

    def _create_user(self, email, password, username=None, **extra_fields):
        """Защищенный метод для создания юзера"""
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, username=None, **extra_fields):
        """Создание обычного юзера"""
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            email, password, username=username, **extra_fields
        )

    def create_superuser(self, email, password=None, username=None, **extra_fields):
        """Создание суперюзера"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields["is_active"] = True

        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, username=None, **extra_fields)


class CustomUser(AbstractUser):
    """Класс отчвечающий за создание юзера в БД"""

    username = models.CharField(blank=True, null=True, max_length=150)
    is_active = models.BooleanField(default=False)
    activate_code = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username", ]

    objects = CustomUserManager()

    @staticmethod
    def generate_activation_code(length: int, number_range: str) -> str:
        """Метод для генерации активационного кода"""
        from django.utils.crypto import get_random_string
        return get_random_string(length, number_range)

    def save(self, *args, **kwargs):
        """Переопределение метода save"""
        self.activate_code = self.generate_activation_code(10, "qwerty123456789")
        return super().save(*args, **kwargs)