from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new User"""
        if not email:
            raise ValueError(_("users must have an email address"))

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True,
                              verbose_name=_('Indirizzo e-mail'))
    nome = models.CharField(
        max_length=255,
        verbose_name=_('Nome'), blank=True,
        )
    # nome = models.CharField(
    #     max_length=255,
    #     verbose_name=_('Nome'), blank=True,
    #     validators=[RegexValidator('A-Za-z',
    #     message="Password should be a combination of Alphabets and Numbers")])
    cognome = models.CharField(max_length=255,
                               verbose_name=_('Cognome'), blank=True)
    telefono = models.CharField(max_length=20,
                                verbose_name=_('Telefono'), blank=True)
    indirizzo = models.CharField(max_length=255,
                                 verbose_name=_('Indirizzo'), blank=True)
    citta = models.CharField(max_length=255,
                             verbose_name=_('Città'), blank=True)
    provincia_ita = models.ForeignKey('Provincia',
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      # related_name = 'provincie',
                                      verbose_name=_('Provincia'),
                                      blank=True)
    provincia_estero = models.CharField(max_length=255,
                                        blank=True,
                                        verbose_name=_('Provincia estero'))
    stato = models.CharField(max_length=2, choices=[
                            ('I', _('Italia')), ('E', _('Estero'))],
                            verbose_name=_('Stato'), blank=True)
    stato_estero = models.CharField(max_length=255,
                                    verbose_name=_('Altro stato'),
                                    blank=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


# class UserDetails(models.Model):
#
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     telefono = models.CharField(max_length=20,
#                                 verbose_name=_('Telefono'))
#     indirizzo = models.CharField(max_length=255,
#                                  verbose_name=_('Indirizzo'))
#     citta = models.CharField(max_length=255,
#                              verbose_name=_('Città'))
#     provincia_ita = models.ForeignKey('Provincia',
#                                       on_delete=models.SET_NULL,
#                                       null=True,
#                                       verbose_name=_('Provincia'))
#     provincia_estero = models.CharField(max_length=255,
#                                         blank=True,
#                                         verbose_name=_('Provincia estero'))
#     stato = models.CharField(max_length=2, choices=[
#                             ('I', _('Italia')), ('E', _('Estero'))],
#                             verbose_name=_('Stato'))
#     stato_estero = models.CharField(max_length=255, blank=True,
#                                     verbose_name=_('Altro stato'))


class Provincia(models.Model):

    nome = models.CharField(max_length=255)
    # Regione = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
