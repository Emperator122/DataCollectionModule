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

    common_formset = pg_forms.CommonForm.get_formset_class(pg_models.Common, pg_forms.CommonForm)
    uchred_law_formset = pg_forms.UchredLawForm.get_formset_class(pg_models.UchredLaw, pg_forms.UchredLawForm)
    fil_info_formset = pg_forms.FilInfoForm.get_formset_class(pg_models.FilInfo, pg_forms.FilInfoForm)
    rep_info_formset = pg_forms.RepInfoForm.get_formset_class(pg_models.RepInfo, pg_forms.RepInfoForm)

    # В случае POST запроса
    if request.method == 'POST':
        # Создаем генератор радела struct
        struct_page_generator = pg.StructPageGenerator(request.user, request.POST, request.FILES)
        struct_page_generator.get_formsets_from_data()  # Строим внутри класса экземпляр formset'a исходя из данных
        if struct_page_generator.validate_formsets():  # Если формсет валиден

            fm.clear_user_storage(request.user.username)  # Очищаем хранилище пользователя
            struct_page_generator.structFormsetObj.get_queryset().delete()  # и все старые записи из бд

            struct_page_generator.save_formsets()  # Сохраняем его в бд + файлы
            struct_page_generator.save_html()  # И сохраняем index.html

        return sh.redirect('/')

    # В случае любого другого запроса
    struct_page_generator = pg.StructPageGenerator(request.user)  # Генератор
    user_struct_formset_obj = struct_page_generator.get_user_formsets()

    return sh.render(request, "home.html", context={
            "arg1": "Emperator12",
            "struct_formset": user_struct_formset_obj,
            'user': request.user,
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
