from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date, timedelta
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
import os
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.db.models import Q
from django.db.models import Count
from django.contrib.auth import logout as auth_logout



def landing(request):
    context = RequestContext(request,
                             {'request': request,
                              'user': request.user})

    return render(request, 'landing/landing.html', context_instance=context)
