from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, password, **kwargs):
        if username is None:
            raise TypeError("Users must have a username.")

        if email is None:
            raise TypeError("Users must have an email address.")

        if password is None:
            raise TypeError("Users must have a password.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staffuser(self, email, username, password):
        user = self.create_user(
            email,
            username,
            password
        )
        user.staff = True
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            email,
            username,
            password
        )
        user.staff = True
        user.superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        db_index=True,
        max_length=150,
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        db_index=True,
        unique=True,
    )
    first_name = models.CharField(
        max_length=150,
        unique=False,
    )
    last_name = models.CharField(
        max_length=150,
        unique=False,
    )

    password = models.CharField(
        max_length=150,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = (
        'email', 'password',
    )

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.superuser

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='target_user',
        verbose_name='user'
    )
    subscribed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed',
        verbose_name='subscribed'
    )

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'subscribed'),
                name='unique subscription'
            ),
        )
