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
    struct_page_generator = pg.StructPageGenerator(request.user)  # Генератор раздела struct
    user_struct_formset_obj, = struct_page_generator.get_user_formsets()

    common_page_generator = pg.CommonPageGenerator(request.user)
    common_fs_obj, uchred_law_fs_obj, fil_info_fs_obj, rep_info_fs_obj = common_page_generator.get_user_formsets()

    return sh.render(request, "home.html", context={
            "struct_formset": user_struct_formset_obj,
            "common": {
                'common_formset': common_fs_obj,
                'uchred_formset': uchred_law_fs_obj,
                'fil_info_formset': fil_info_fs_obj,
                'rep_info_formset': rep_info_fs_obj,
            },
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
