from django.template.loader import render_to_string
from django.http import HttpResponse
import django.shortcuts as sh

from .forms import StructForm
from .models import Struct
from .forms import CommonForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
import DataCollectionModuleDjango.mainPage.utils.file_manager as fm
import django.contrib.auth as auth
import os
import DataCollectionModuleDjango.mainPage.utils.page_generator as pg
from django.forms import modelformset_factory


def home_page(request):
    if not request.user.is_authenticated:
        return sh.redirect('/login')
    struct_objects = Struct.objects.filter(owner=request.user)
    struct_formset_obj = modelformset_factory(Struct, form=StructForm, extra=0 if len(struct_objects) > 0 else 1)

    # Если на сервер отправил данные авторизованный пользователь
    if request.method == 'POST' and request.user.is_authenticated:
        # Очищаем его хранилище
        fm.clear_user_storage(request.user.username)

        # Генерация раздела структура органов управления
        struct_formset = struct_formset_obj(prefix="struct", data=request.POST, files=request.FILES)  # Данные с формы
        if struct_formset.is_valid():
            # Очищаем старые данные, введенные юзером
            Struct.objects.filter(owner=request.user).delete()
            # Сохраняем каждую форму из набора на серв
            for f in struct_formset:
                f.save(user=request.user)
            # Сохраняем данные
            pg.StructPageGenerator(struct_formset).save_html(request.user)

            return sh.redirect('/')

    is_logged_in = request.user.is_authenticated
    if is_logged_in:
        user = request.user
    else:
        user = None

    struct_formset = struct_formset_obj(prefix="struct", queryset=struct_objects)
    common_form = CommonForm(prefix="common")

    return sh.render(request, "home.html", context={
        "arg1": "Emperator12",
        "struct_formset": struct_formset,
        "common_form": common_form,
        'user': user,
        'is_logged_in': is_logged_in,
    })


def login_page(request):
    if request.user.is_authenticated:
        return sh.redirect('/')

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                auth.login(request, user)
                return sh.redirect('/')
    else:
        form = AuthenticationForm()

    return sh.render(request, "login.html", context={
        "authForm": form
    })


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return sh.redirect('/')
