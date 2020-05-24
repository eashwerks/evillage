from django.shortcuts import render, redirect


def index_view(request):
    return render(request, 'app_0/index.html')


def req_ration_card_view(request):
    context = {}
    template_name = 'app_0/ration_card.html'
    if request.method == 'GET':
        return render(request, template_name, context)
    if request.method == 'POST':
        print(request.POST)
        return render(request, template_name, context)


def req_nativity_view(request):
    return render(request, 'app_0/nativity.html')


def req_income_view(request):
    return render(request, 'app_0/income.html')


def req_identity_card_view(request):
    return render(request, 'app_0/identity.html')


def req_cast_view(request):
    return render(request, 'app_0/cast.html')


def req_tax_view(request):
    return render(request, 'app_0/paytax.html')


def req_complaint_view(request):
    return render(request, 'app_0/complaint.html')


def start(request):
    return redirect(index_view)
