from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date, timedelta
from django.contrib.auth.models import  Group
from django.core.mail import send_mail
import os
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.db.models import Q
from django.db.models import Count
from django.contrib.auth import logout as auth_logout
from .models import brandContact
from advoclik.models import MyUser


# ----------------------- #
#      GENERAL/STATIC     #
# ----------------------- #

def landing(request):
    context = RequestContext(request,
                             {'request': request,
                              'user': request.user})

    return render(request, 'landing/landing.html', context_instance=context)

def about(request):
    context = RequestContext(request,
                             {'request': request,
                              'user': request.user})

    return render(request, 'landing/about.html', context_instance=context)

def company(request):
    context = RequestContext(request,
                             {'request': request,
                              'user': request.user})

    return render(request, 'landing/company.html', context_instance=context)


# --------------- #
#      BRANDS     #
# --------------- #
def brands(request):
    all_brands = brandContact.objects.all
    context = RequestContext(request,
                             {'request': request,
                              'user': request.user,
                              'all_brands': all_brands})

    return render(request, 'landing/brands.html', context_instance=context)

def add_brand_contact(request):
    POST = request.POST

    # Pull values from the POST
    contact_name = POST['contact_name']
    contact_email = POST['contact_email']
    brand = POST['company']

    # Add brand contact to the db if not there
    brand_contact, created = brandContact.objects.get_or_create(contact_name=contact_name,
                                                                contact_email = contact_email,
                                                                company=brand)
    return HttpResponseRedirect(reverse('landing:brands'))


# --------------------- #
#      REGISTRATION     #
# --------------------- #

def register(request):
    context = RequestContext(request,
                             {'request': request,
                              'user': request.user})

    return render(request, 'landing/register.html', context_instance=context)

def register_user(request):
    POST = request.POST
    first_name = POST['first_name']
    last_name = POST['last_name']
    password = POST['password1']
    email = POST['email']
    user = MyUser.objects.get_or_create(first_name=first_name,
                                        last_name=last_name,
                                        email=email,
                                        password=password)

    return HttpResponseRedirect('/home')
