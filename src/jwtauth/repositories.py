from core.repositories import BaseRepository, ObjectDoesNotExist
from .models import CustomUser, Profile, RefreshToken, QRCode


class UserRepository(BaseRepository):
    model = CustomUser

    @classmethod
    def get(cls, email):
        try:
            return cls.model.objects.get(email=email)
        except ObjectDoesNotExist:
            return None

    @classmethod
    def update(cls, instance, **kwargs):
        password = kwargs.pop('password', None)
        for key, value in kwargs.items():
            setattr(instance, key, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class ProfileRepository(BaseRepository):
    model = Profile

    @classmethod
    def get_by_user(cls, user):
        return cls.model.objects.get(user=user)


class RefreshTokenRepository(BaseRepository):
    model = RefreshToken

    @classmethod
    def get(cls, token):
        return cls.model.objects.get(token=token)


class QRCodeRepository(BaseRepository):
    model = QRCode

    @classmethod
    def get(cls, user):
        return cls.model.objects.get(user=user)
