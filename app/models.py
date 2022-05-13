from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# from s3direct.fields import S3DirectField
from s3upload.fields import S3UploadField

#custom user manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2=None, image=None):
        """
        Creates and saves a User with the given email, name
        and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            image=image,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None,image=None):
        """
        Creates and saves a superuser with the given email, name
        and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            image=image,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

def user_directory_path(instance, filename):
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'blog_image/{0}/{1}'.format(instance.email,filename)
#Custom user model
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path,null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin