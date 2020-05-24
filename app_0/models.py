from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.validators import RegexValidator
from django.db import models

from model_utils import Choices
from model_utils.fields import StatusField


class VillageOfficer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=32, unique=True)
    phone_number = models.CharField(max_length=24)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return self.username


class RequestUser(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(validators=[phone_regex], max_length=17)

    def __str__(self):
        return self.name


class AbstractModel(models.Model):
    STATUS = Choices('PENDING', 'APPROVED', 'REJECTED')

    requested_by = models.ForeignKey(RequestUser, on_delete=models.CASCADE)
    requested_on = models.DateField(auto_created=True)
    status = StatusField(choices_name='STATUS', default=STATUS.PENDING)

    class Meta:
        abstract = True


class RationCardService(AbstractModel):
    number = models.CharField(max_length=20)
    panchayath = models.CharField(max_length=120)
    taluk = models.CharField(max_length=120)
    ward = models.CharField(max_length=120)
    house_name = models.CharField(max_length=120)
    house_number = models.CharField(max_length=10)
    card_holder_name = models.CharField(max_length=120)
    card_holder_photo = models.FileField(upload_to='ration_card')
    pin_code = models.CharField(max_length=6)
    annual_income = models.DecimalField(max_digits=9, decimal_places=2)
    address = models.TextField()

    def __str__(self):
        return self.number


class NativityService(AbstractModel):
    number = models.CharField(max_length=20)
    dob = models.DateField()
    pob = models.CharField(max_length=12)
    uid = models.CharField(max_length=120)
    nationality = models.CharField(max_length=120)
    father = models.CharField(max_length=10)
    mother = models.CharField(max_length=120)
    photo = models.FileField(upload_to='Nativity/')
    document = models.FileField(upload_to='Nationality/')
    passport_number = models.CharField(max_length=6)
    poi = models.CharField(max_length=120)
    doi = models.DateField()
    validity = models.DateField()
    address = models.TextField()

    def __str__(self):
        return self.number


class IncomeService(AbstractModel):
    number = models.CharField(max_length=20)
    dob = models.DateField()
    pob = models.CharField(max_length=12)
    uid = models.CharField(max_length=120)
    father = models.CharField(max_length=10)
    mother = models.CharField(max_length=120)
    annual_income = models.DecimalField(max_digits=9, decimal_places=2)
    photo = models.FileField(upload_to='Nativity/')
    document = models.FileField(upload_to='Nationality/')
    address = models.TextField()

    def __str__(self):
        return self.number


class IdentityService(AbstractModel):
    number = models.CharField(max_length=20)
    dob = models.DateField()
    pob = models.CharField(max_length=12)
    uid = models.CharField(max_length=120)
    father = models.CharField(max_length=10)
    mother = models.CharField(max_length=120)
    designation = models.CharField(max_length=120)
    g_name = models.CharField(max_length=120)
    g_relation = models.CharField(max_length=120)
    g_uid = models.CharField(max_length=120)
    photo = models.FileField(upload_to='id/')
    g_photo = models.FileField(upload_to='id_g/')
    document = models.FileField(upload_to='id/')
    address = models.TextField()

    def __str__(self):
        return self.number


class CastService(AbstractModel):
    number = models.CharField(max_length=20)
    dob = models.DateField()
    pob = models.CharField(max_length=12)
    uid = models.CharField(max_length=120)
    father = models.CharField(max_length=10)
    mother = models.CharField(max_length=120)
    cast = models.CharField(max_length=120)
    photo = models.FileField(upload_to='Nativity/')
    document = models.FileField(upload_to='Nationality/')
    address = models.TextField()

    def __str__(self):
        return self.number


class TaxService(AbstractModel):
    number = models.CharField(max_length=20)
    tax_number = models.CharField(max_length=120)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.number


class ComplaintService(AbstractModel):
    number = models.CharField(max_length=20)
    title = models.CharField(max_length=120)
    service = models.CharField(max_length=120)
    message = models.TextField()

    def __str__(self):
        return self.number


class NotificationService(models.Model):
    title = models.CharField(max_length=120)
    message = models.TextField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
