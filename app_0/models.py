from django.core.validators import RegexValidator
from django.db import models

from model_utils import Choices
from model_utils.fields import StatusField


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


class Request(models.Model):
    STATUS = Choices('PENDING', 'APPROVED', 'REJECTED')
    TYPE = Choices('RATION_CARD', 'NATIVITY', 'INCOME', 'IDENTITY', 'CAST', 'TAX')

    number = models.CharField(max_length=20)
    requested_by = models.ForeignKey(RequestUser, on_delete=models.CASCADE)
    requested_on = models.DateField(auto_created=True)
    status = StatusField(choices_name='STATUS', default=STATUS.PENDING)
    type = StatusField(choices_name='TYPE', default=TYPE.RATION_CARD)

    '''for RATION_CARD'''
    panchayath = models.CharField(max_length=120, null=True, blank=True)
    taluk = models.CharField(max_length=120, null=True, blank=True)
    ward = models.CharField(max_length=120, null=True, blank=True)
    house_name = models.CharField(max_length=120, null=True, blank=True)
    card_holder_name = models.CharField(max_length=120, null=True, blank=True)
    card_holder_photo = models.ImageField(upload_to='ration_card', null=True, blank=True)
    pin_code = models.CharField(max_length=6, null=True, blank=True)
    annual_income = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)

    address = models.TextField()

    def __str__(self):
        return self.number

    def save(self, **kwargs):
        if not self.id:
            if self.status == 'RATION_CARD':
                self._check_rc_fields()
        return super(Request, self).save(**kwargs)

    def _check_rc_fields(self):
        if not (self.panchayath, self.taluk, self.ward, self.house_name, self.card_holder_name, self.card_holder_photo,
                self.pin_code, self.annual_income):
            raise Exception('All fields for Ration card is required.')
