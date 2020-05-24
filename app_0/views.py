import random
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, redirect
from django.utils import timezone

from app_0.forms import RequestUserForm
from app_0.models import RationCardService, RequestUser, NativityService, IncomeService, IdentityService, CastService, \
    TaxService, ComplaintService, NotificationService


def index_view(request):
    context = {'notifications': NotificationService.objects.all()}
    return render(request, 'app_0/index.html', context)


def req_ration_card_view(request):
    context = {}
    template_name = 'app_0/ration_card.html'
    if request.method == 'GET':
        return render(request, template_name, context)
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        panchayath = request.POST.get('pmc', None)
        taluk = request.POST.get('taluk', None)
        ward = request.POST.get('ward', None)
        card_holder_name = request.POST.get('c-name', None)
        house_name = request.POST.get('hname', None)
        address = request.POST.get('address', None)
        house_number = request.POST.get('hnumber', None)
        pin_code = request.POST.get('pincode', None)
        annual_income = request.POST.get('annual-income', None)
        card_holder_photo = request.FILES.get('pic', None)
        try:
            number = timezone.now().strftime("%Y%m%d") + 'RC' + str(random.randint(1, 100))
            user, created = RequestUser.objects.get_or_create(name=name, email=email, phone=phone)
            RationCardService.objects.create(number=number, requested_by=user,
                                             panchayath=panchayath,
                                             taluk=taluk, ward=ward, house_number=house_number, house_name=house_name,
                                             card_holder_name=card_holder_name, pin_code=pin_code,
                                             annual_income=Decimal(annual_income), address=address,
                                             requested_on=timezone.now().date(), card_holder_photo=card_holder_photo)
            messages.add_message(request, messages.SUCCESS,
                                 'Request successfully registered. Please check your mail {}'.format(email))
            return redirect(index_view)
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
        return render(request, template_name, context)


def req_nativity_view(request):
    context = {}
    template_name = 'app_0/nativity.html'
    if request.method == 'GET':
        return render(request, template_name, context)
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        dob = request.POST.get('dob', None)
        pob = request.POST.get('pob', None)
        uid = request.POST.get('uid', None)
        nationality = request.POST.get('nationality', None)
        father = request.POST.get('father', None)
        mother = request.POST.get('mother', None)
        address = request.POST.get('address', None)
        photo = request.FILES.get('photo', None)
        document = request.FILES.get('proof', None)
        passport_number = request.POST.get('passport_number', None)
        poi = request.POST.get('poi', None)
        doi = request.POST.get('doi', None)
        validity = request.POST.get('validity', None)
        try:
            number = timezone.now().strftime("%Y%m%d") + 'NA' + str(random.randint(1, 100))
            user, created = RequestUser.objects.get_or_create(name=name, email=email, phone=phone)
            NativityService.objects.create(number=number, requested_by=user, address=address,
                                           requested_on=timezone.now().date(), dob=dob, pob=pob, uid=uid,
                                           nationality=nationality, father=father, mother=mother, photo=photo,
                                           document=document, passport_number=passport_number, poi=poi, doi=doi,
                                           validity=validity)
            messages.add_message(request, messages.SUCCESS,
                                 'Request successfully registered. Please check your mail {}'.format(email))
            return redirect(index_view)
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
        return render(request, template_name, context)


def req_income_view(request):
    context = {}
    template_name = 'app_0/income.html'
    if request.method == 'GET':
        return render(request, template_name, context)
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        dob = request.POST.get('dob', None)
        pob = request.POST.get('pob', None)
        uid = request.POST.get('uid', None)
        father = request.POST.get('father', None)
        mother = request.POST.get('mother', None)
        address = request.POST.get('address', None)
        annual_income = request.POST.get('annual_income', None)
        photo = request.FILES.get('photo', None)
        document = request.FILES.get('proof', None)
        try:
            number = timezone.now().strftime("%Y%m%d") + 'IN' + str(random.randint(1, 100))
            user, created = RequestUser.objects.get_or_create(name=name, email=email, phone=phone)
            IncomeService.objects.create(number=number, requested_by=user, address=address,
                                         requested_on=timezone.now().date(), dob=dob, pob=pob, uid=uid, father=father,
                                         mother=mother, photo=photo,
                                         document=document, annual_income=annual_income)
            messages.add_message(request, messages.SUCCESS,
                                 'Request successfully registered. Please check your mail {}'.format(email))
            return redirect(index_view)
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
        return render(request, template_name, context)


def req_identity_card_view(request):
    context = {}
    template_name = 'app_0/identity.html'
    if request.method == 'GET':
        return render(request, template_name, context)
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        dob = request.POST.get('dob', None)
        pob = request.POST.get('pob', None)
        uid = request.POST.get('uid', None)
        father = request.POST.get('father', None)
        mother = request.POST.get('mother', None)
        address = request.POST.get('address', None)
        designation = request.POST.get('designation', None)
        g_name = request.POST.get('g_name', None)
        g_relation = request.POST.get('g_relation', None)
        g_uid = request.POST.get('g_uid', None)
        g_photo = request.FILES.get('g_photo', None)
        photo = request.FILES.get('photo', None)
        document = request.FILES.get('proof', None)
        try:
            number = timezone.now().strftime("%Y%m%d") + 'ID' + str(random.randint(1, 100))
            user, created = RequestUser.objects.get_or_create(name=name, email=email, phone=phone)
            IdentityService.objects.create(number=number, requested_by=user, address=address,
                                           requested_on=timezone.now().date(), dob=dob, pob=pob, uid=uid, father=father,
                                           mother=mother, photo=photo, designation=designation,
                                           document=document, g_name=g_name, g_relation=g_relation, g_uid=g_uid,
                                           g_photo=g_photo)
            messages.add_message(request, messages.SUCCESS,
                                 'Request successfully registered. Please check your mail {}'.format(email))
            return redirect(index_view)
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
        return render(request, template_name, context)


def req_cast_view(request):
    context = {}
    template_name = 'app_0/cast.html'
    if request.method == 'GET':
        return render(request, template_name, context)
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        dob = request.POST.get('dob', None)
        pob = request.POST.get('pob', None)
        uid = request.POST.get('uid', None)
        father = request.POST.get('father', None)
        mother = request.POST.get('mother', None)
        address = request.POST.get('address', None)
        cast = request.POST.get('cast', None)
        photo = request.FILES.get('photo', None)
        document = request.FILES.get('proof', None)
        try:
            number = timezone.now().strftime("%Y%m%d") + 'CA' + str(random.randint(1, 100))
            user, created = RequestUser.objects.get_or_create(name=name, email=email, phone=phone)
            CastService.objects.create(number=number, requested_by=user, address=address,
                                       requested_on=timezone.now().date(), dob=dob, pob=pob, uid=uid, father=father,
                                       mother=mother, photo=photo,
                                       document=document, cast=cast)
            messages.add_message(request, messages.SUCCESS,
                                 'Request successfully registered. Please check your mail {}'.format(email))
            return redirect(index_view)
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
        return render(request, template_name, context)


def req_tax_view(request):
    context = {}
    template_name = 'app_0/paytax.html'
    if request.method == 'GET':
        return render(request, template_name, context)
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        tax_number = request.POST.get('tax_number', None)
        tax_amount = request.POST.get('tax_amount', None)
        try:
            number = timezone.now().strftime("%Y%m%d") + 'TA' + str(random.randint(1, 100))
            user, created = RequestUser.objects.get_or_create(name=name, email=email, phone=phone)
            TaxService.objects.create(number=number, requested_on=timezone.now().date(), requested_by=user,
                                      tax_amount=tax_amount, tax_number=tax_number)
            messages.add_message(request, messages.SUCCESS,
                                 'Request successfully payed your tax. Please check your mail {}'.format(email))
            return redirect(index_view)
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
        return render(request, template_name, context)


def req_complaint_view(request):
    context = {}
    template_name = 'app_0/complaint.html'
    if request.method == 'GET':
        return render(request, template_name, context)
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        title = request.POST.get('title', None)
        service = request.POST.get('service', None)
        message = request.POST.get('message', None)
        try:
            number = timezone.now().strftime("%Y%m%d") + 'CO' + str(random.randint(1, 100))
            user, created = RequestUser.objects.get_or_create(name=name, email=email, phone=phone)
            ComplaintService.objects.create(number=number, requested_on=timezone.now().date(), requested_by=user,
                                            title=title, service=service, message=message)
            messages.add_message(request, messages.SUCCESS,
                                 'Complaint successfully registered. Please check your mail {}'.format(email))
            return redirect(index_view)
        except Exception as err:
            messages.add_message(request, messages.ERROR, err)
        return render(request, template_name, context)


def start(request):
    return redirect(index_view)


def login_view(request):
    context = {}
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        try:
            if username and password:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                else:
                    error_message = 'Check username and password'

            else:
                error_message = 'username and password required'
        except:
            error_message = 'Check username and password'
        if error_message:
            messages.add_message(request, messages.ERROR, error_message)

    return redirect(start)


def logout_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
    return redirect(start)


def dashboard(request):
    context = {}
    template_name = 'admin/dashboard.html'
    return render(request, template_name, context)
