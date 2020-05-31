from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import loader

from model_utils import Choices
from model_utils.fields import StatusField

from app_0.certificate_gen import render_to_pdf
from app_0.email import thread_mail


class Village(models.Model):
    name = models.CharField(max_length=120)
    address = models.TextField()

    def __str__(self):
        return '{}-{}'.format(self.name, self.address)


class VillageOfficer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=32, unique=True)
    phone_number = models.CharField(max_length=24)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'phone_number']

    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=True)

    objects = UserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.is_staff:
            if not self.village:
                raise Exception('Village is required.')
        return super(VillageOfficer, self).save(*args, **kwargs)


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
    village = models.ForeignKey(Village, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class RationCardService(AbstractModel):
    type = models.CharField(max_length=120, default='Ration card')
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
    type = models.CharField(max_length=120, default='Nativity')
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
    type = models.CharField(max_length=120, default='Income')
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
    type = models.CharField(max_length=120, default='Identity card')
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
    type = models.CharField(max_length=120, default='Caste')
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
    type = models.CharField(max_length=120, default='Tax')
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


@receiver(post_save, sender=TaxService)
def my_handler1(sender, instance, **kwargs):
    if instance.status == 'PENDING':
        subject = '{} {} Paid.'.format(instance.type, instance.number)
        body = ''
        form_email = settings.EMAIL_HOST_USER
        to_email = instance.requested_by.email
        html = loader.render_to_string(
            'email/email.html',
            {
                'title': "Payment Success.",
                'content': " Your tax payment of {} successfully registered with number {}".format(instance.tax_amount,
                                                                                                   instance.tax_number)
            }
        )
        thread_mail(subject, body, form_email, [to_email], False, html)


@receiver(post_save, sender=RationCardService)
def my_handler2(sender, instance, **kwargs):
    if instance.status == 'PENDING':
        subject = '{} {} Requested.'.format(instance.type, instance.number)
        body = ''
        form_email = settings.EMAIL_HOST_USER
        to_email = instance.requested_by.email
        html = loader.render_to_string(
            'email/email.html',
            {
                'title': subject,
                'content': "Request registered and wait for approval"
            }
        )
        thread_mail(subject, body, form_email, [to_email], False, html)
    if instance.status == 'REJECTED':
        rejected_mail(instance)
    if instance.status == 'APPROVED':
        subject = '{} with number {} APPROVED.'.format(instance.type, instance.number)
        body = ''
        form_email = settings.EMAIL_HOST_USER
        to_email = instance.requested_by.email
        html = loader.render_to_string(
            'email/email.html',
            {
                'title': subject,
                'content': "Your {} number {} is approved. It will be sent to your address".format(instance.type,
                                                                                                   instance.number)
            }
        )
        thread_mail(subject, body, form_email, [to_email], False, html)


@receiver(post_save, sender=IncomeService)
def my_handler3(sender, instance, **kwargs):
    if instance.status == 'PENDING':
        subject = '{} {} Requested.'.format(instance.type, instance.number)
        body = ''
        form_email = settings.EMAIL_HOST_USER
        to_email = instance.requested_by.email
        html = loader.render_to_string(
            'email/email.html',
            {
                'title': subject,
                'content': "Request registered and wait for approval"
            }
        )
        thread_mail(subject, body, form_email, [to_email], False, html)
    if instance.status == 'APPROVED':
        subject = '{} with number {} APPROVED.'.format(instance.type, instance.number)
        body = ''
        form_email = settings.EMAIL_HOST_USER
        to_email = instance.requested_by.email
        attachment = render_to_pdf(instance, 'admin/certificate.html')
        html = loader.render_to_string(
            'email/email.html',
            {
                'title': subject,
                'content': "Your {} number {} is approved. The certificate is attached".format(instance.type,
                                                                                               instance.number)
            }
        )
        thread_mail(subject, body, form_email, [to_email], False, html, attachment)
    if instance.status == 'REJECTED':
        rejected_mail(instance)


@receiver(post_save, sender=CastService)
def my_handler4(sender, instance, **kwargs):
    if instance.status == 'PENDING':
        subject = '{} {} Requested.'.format(instance.type, instance.number)
        body = ''
        form_email = settings.EMAIL_HOST_USER
        to_email = instance.requested_by.email
        html = loader.render_to_string(
            'email/email.html',
            {
                'title': subject,
                'content': "Request registered and wait for approval"
            }
        )
        thread_mail(subject, body, form_email, [to_email], False, html)
    if instance.status == 'APPROVED':
        subject = '{} with number {} APPROVED.'.format(instance.type, instance.number)
        body = ''
        form_email = settings.EMAIL_HOST_USER
        to_email = instance.requested_by.email
        attachment = render_to_pdf(instance, 'admin/certificate.html')
        html = loader.render_to_string(
            'email/email.html',
            {
                'title': subject,
                'content': "Your {} number {} is approved. The certificate is attached".format(instance.type,
                                                                                               instance.number)
            }
        )
        thread_mail(subject, body, form_email, [to_email], False, html, attachment)
    if instance.status == 'REJECTED':
        rejected_mail(instance)


@receiver(post_save, sender=IdentityService)
def my_handler5(sender, instance, **kwargs):
    if instance.status == 'PENDING':
        subject = '{} {} Requested.'.format(instance.type, instance.number)
        body = ''
        form_email = settings.EMAIL_HOST_USER
        to_email = instance.requested_by.email
        html = loader.render_to_string(
            'email/email.html',
            {
                'title': subject,
                'content': "Request registered and wait for approval"
            }
        )
        thread_mail(subject, body, form_email, [to_email], False, html)
    if instance.status == 'APPROVED':
        subject = '{} with number {} APPROVED.'.format(instance.type, instance.number)
        body = ''
        form_email = settings.EMAIL_HOST_USER
        to_email = instance.requested_by.email
        html = loader.render_to_string(
            'email/email.html',
            {
                'title': subject,
                'content': "Your {} number {} is approved. It will be sent to your address".format(instance.type,
                                                                                                   instance.number)
            }
        )
        thread_mail(subject, body, form_email, [to_email], False, html)
    if instance.status == 'REJECTED':
        rejected_mail(instance)


@receiver(post_save, sender=NativityService)
def my_handler6(sender, instance, **kwargs):
    if instance.status == 'PENDING':
        subject = '{} {} Requested.'.format(instance.type, instance.number)
        body = ''
        form_email = settings.EMAIL_HOST_USER
        to_email = instance.requested_by.email
        html = loader.render_to_string(
            'email/email.html',
            {
                'title': subject,
                'content': "Request registered and wait for approval"
            }
        )
        thread_mail(subject, body, form_email, [to_email], False, html)
    if instance.status == 'APPROVED':
        subject = '{} with number {} APPROVED.'.format(instance.type, instance.number)
        body = ''
        form_email = settings.EMAIL_HOST_USER
        to_email = instance.requested_by.email
        attachment = render_to_pdf(instance, 'admin/certificate.html')
        html = loader.render_to_string(
            'email/email.html',
            {
                'title': subject,
                'content': "Your {} number {} is approved. The certificate is attached".format(instance.type,
                                                                                               instance.number)
            }
        )
        thread_mail(subject, body, form_email, [to_email], False, html, attachment)
    if instance.status == 'REJECTED':
        rejected_mail(instance)


def rejected_mail(instance):
    subject = '{} {} is Rejected.'.format(instance.type, instance.number)
    body = ''
    form_email = settings.EMAIL_HOST_USER
    to_email = instance.requested_by.email
    html = loader.render_to_string(
        'email/email.html',
        {
            'title': subject,
            'content': "Request is rejected by the village officer, please contact village office."
        }
    )
    thread_mail(subject, body, form_email, [to_email], False, html)
