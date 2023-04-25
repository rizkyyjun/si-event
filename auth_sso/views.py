from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from django.contrib import messages
from .utils import get_sso_ui_data
from account.models import Account, User
from django.contrib.auth import authenticate, login
from .models import SSOUIAccount

import requests

from .utils import get_sso_ui_data
from django.views.decorators.csrf import csrf_exempt

def login_sso(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        sso_data = get_sso_ui_data(
            username=username,
            password=password
        ).json()

        if sso_data['state'] == 0:
            messages.info(request, 'Wrong SSO UI credentials')
            return redirect('auth_sso:login_sso')
        else:
            # Account belum terbuat
            if not SSOUIAccount.objects.filter(username=username).exists():
                email = f'{username}@ui.ac.id'
                user = User.objects.create_user(username=username, password=password, email=email)
                accountSSO = SSOUIAccount(
                    user = user,
                    kode_identitas = sso_data['kodeidentitas'],
                    nama = sso_data['nama'],
                    kode_organisasi = sso_data['kode_org'].split(":")[0],
                    username = username,
                    role = 'Guest'
                )
                acc = Account(
                    user = user,
                    accSSO = accountSSO,
                    username = username,
                    email = email,
                    role = 'Guest',
                    accountType = 'SSO UI'
                )
                user.save()
                accountSSO.save()
                acc.save()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home')

    context = {'form':'form'}
    return render(request, 'login_sso.html', context)