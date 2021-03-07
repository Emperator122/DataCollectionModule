from django.http import HttpResponse
import django.shortcuts as sh
from django.contrib.auth.forms import AuthenticationForm
import DataCollectionModuleDjango.mainPage.models as pg_models
import DataCollectionModuleDjango.mainPage.forms as pg_forms
import DataCollectionModuleDjango.mainPage.utils.file_manager as fm
import django.contrib.auth as auth
import DataCollectionModuleDjango.mainPage.utils.page_generator as pg


def home_page(request):
    if not request.user.is_authenticated:
        return sh.redirect('/login')

    struct_formset_obj = pg_forms.StructForm.get_formset(pg_models.Struct, pg_forms.StructForm)
    common_formset_obj = pg_forms.CommonForm.get_formset(pg_models.Common, pg_forms.CommonForm)
    uchred_law_formset_obj = pg_forms.UchredLawForm.get_formset(pg_models.UchredLaw, pg_forms.UchredLawForm)
    fil_info_formset_obj = pg_forms.FilInfoForm.get_formset(pg_models.FilInfo, pg_forms.FilInfoForm)
    rep_info_formset_obj = pg_forms.RepInfoForm.get_formset(pg_models.RepInfo, pg_forms.RepInfoForm)

    # Если на сервер отправил данные авторизованный пользователь
    if request.method == 'POST' and request.user.is_authenticated:
        # Очищаем его хранилище
        fm.clear_user_storage(request.user.username)

        # Генерация раздела структура органов управления
        struct_formset = struct_formset_obj(prefix="struct", data=request.POST, files=request.FILES)  # Данные с формы
        if struct_formset.is_valid():
            # Очищаем старые данные, введенные юзером
            struct_formset.get_queryset().delete()
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

    struct_formset = pg_forms.StructForm.get_owned_formset(request.user, pg_models.Struct, pg_forms.StructForm,
                                                           prefix="struct")
    common_form = pg_forms.CommonForm.get_owned_formset(request.user, pg_models.Struct, pg_forms.StructForm,
                                                        prefix="common")

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
