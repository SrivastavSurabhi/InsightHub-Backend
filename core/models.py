from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime

class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **other_fields):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(username=username, email=self.normalize_email(email), **other_fields )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staffuser(self, username, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email=None):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.create_staffuser(username=username, email=email, password=password)
        user.email = email
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.role = "admin"
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    __doc__ = ''' user model '''
    userType = ((1, "admin"), (2, "user"))
    firstName = models.CharField(max_length=30, blank=True)
    lastName = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    email = models.EmailField(null=True, blank=True, unique=True, db_index=True)
    isActive = models.BooleanField(default=True)
    userRole = models.IntegerField(choices=userType, default=2)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    createdBy = models.IntegerField(default=1)
    createdOnUtc = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    modifiedBy = models.IntegerField(default=1)
    modifiedOnUtc = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

class Genres(models.Model):
    genreTypes = ((1, 'People'),(2, 'Media'),)
    genreId = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000, null=True, blank=True)
    genreImagePath = models.CharField(max_length=500, null=True, blank=True)
    genreType = models.IntegerField(choices=genreTypes)
    createdBy = models.IntegerField()
    createdOnUtc = models.DateTimeField(auto_now_add=True)
    modifiedBy = models.IntegerField()
    modifiedOnUtc = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False)


class Exceptions(models.Model):
    exceptionId = models.BigAutoField(primary_key=True)
    stackTrace = models.TextField(null=True, blank=True)
    message = models.CharField(max_length=1000, null=True, blank=True)
    occuredOnUtc = models.DateTimeField(auto_now_add=True)
    errorType = models.CharField(max_length=1000, null=True, blank=True)
    exceptionMethod = models.CharField(max_length=1000, null=True, blank=True)
