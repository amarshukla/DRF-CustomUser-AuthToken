from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_complete_user(self, 
                            username, 
                            email, 
                            phone, 
                            user_type,
                            location,
                            team_name=None,
                            skill=None,
                            password=None):
        if not phone:
            raise ValueError('Users must have a phone')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=UserManager.normalize_email(email),
            phone=phone,
            password=password,
            user_type=user_type,
            location=location,
            team_name=team_name,
            skill=skill
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$'


class User(AbstractBaseUser):
    
    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'candidate'),
        (3, 'hr'),
    )
    username = models.CharField(max_length=255, unique=True, validators=[RegexValidator(
        regex=USERNAME_REGEX,
        message='name must be Alphanumeric or contain any of the following: ". @ + -" ',
        code='invalid_name'
    )])
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)
    phone = models.CharField(max_length=10, blank=False, unique=True)
    team_name = models.CharField(max_length=50, blank=True, null=True)
    skill = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=30, blank=False)


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        user_name = self.username
        if user_name == "":
            return self.email
        else:
            return user_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
