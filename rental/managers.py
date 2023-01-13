from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, password, phone, email,
                    is_admin=False, is_staff=False, is_active=False, login=''):

        if not phone:
            raise ValueError("User must have a phone number")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(phone=phone)
        user.set_password(password)
        user.email = email
        user.login = login
        user.is_admin = is_admin
        user.is_staff = is_staff
        user.is_active = is_active
        user.is_superuser = False
        user.save()

        return user

    def create_superuser(self, password, phone, email):
        if not phone:
            raise ValueError("User must have a phone number")
        if not password:
            raise ValueError("User must have a password")

        user = self.create_user(password, email, phone, is_admin=True, is_staff=True, is_active=True)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.email = email
        user.save()
        return user
