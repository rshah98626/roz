"""File outlining all the models in the user application."""
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    """Custom User implementation."""

    pass
