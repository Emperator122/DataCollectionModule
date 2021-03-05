from django.core.files.uploadedfile import UploadedFile
from django.template.loader import render_to_string
from django.http import HttpResponse
import django.shortcuts as sh
from django.utils.datastructures import MultiValueDict

from .forms import StructForm
from .forms import CommonForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
import django.contrib.auth as auth
import os
from django.forms import formset_factory


def home_page(request):
    struct_formset_obj = formset_factory(StructForm)

    # Если на сервер отправил данные авторизованный пользователь
    if request.method == 'POST' and request.user.is_authenticated:
        # Очищаем его хранилище
        clear_user_storage(request.user.username)

        # Генерация раздела структура органов управления
        struct_formset = struct_formset_obj(prefix="struct", data=request.POST, files=request.FILES)  # Данные с формы

        # Генерация конктекса для передачи в template
        struct_context = {"meta": {
            "structOrgUprav": []
        }}
        if struct_formset.is_valid():
            for f in struct_formset:  # Для каждой формы в наборе
                # Получим чистые данные
                form_data = f.cleaned_data

                # Загрузим файл на сервер
                division_clause_doc_link = handle_uploaded_file(form_data.get("divisionClauseDocLink"),
                                                                request.user.username)

                # Добавим данные в контекст на основе переданных полей
                struct_context["meta"]["structOrgUprav"].append({
                    "children": {
                        "name": {
                                "value": form_data.get("name")
                            },
                        "fio": {
                            "value": form_data.get("fio")
                        },
                        "post": {
                            "value": form_data.get("post")
                        },
                        "addressStr": {
                            "value": form_data.get("addressStr")
                        },
                        "site": {
                            "value": form_data.get("site")
                        },
                        "email": {
                            "value": form_data.get("email")
                        },
                        "divisionClauseDocLink": {
                            "href": os.path.join("..", "files", division_clause_doc_link),
                            "value": "Ссылка"
                        },
                    }
                })

        # Рендерим данные для html
        html = render_to_string("pageGenerator/struct.html", context=struct_context)

        # Сохраняем их в соотвествующую папку
        fs = FileSystemStorage("fileStore/"+request.user.username)
        os.mkdir(os.path.join(fs.location, "struct"))
        with fs.open(os.path.join(fs.location, "structOrgUprav", "index.html"), 'wb') as destination:
            destination.write(html.encode('utf-8'))

        return sh.redirect('/')

    is_logged_in = request.user.is_authenticated
    if is_logged_in:
        user = request.user
    else:
        user = None

    struct_formset = struct_formset_obj(prefix="struct")
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


def clear_user_storage(user_id):
    # Экземпляр FileSystemStorage
    fs = FileSystemStorage("fileStore")
    # Если пользователь когда-либо уже загружал файлы, то уничтожаем их...
    if os.path.exists(fs.location + '/' + user_id):
        for root, dirs, files in os.walk(fs.location + '/' + user_id, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(fs.location + '/' + user_id)  # ...вместе с директорией пользователя
    os.mkdir(fs.location + '/' + user_id)  # Затем пересоздаем директорию пользователя
    os.mkdir(os.path.join(fs.location, user_id, "files"))  # Затем пересоздаем директорию пользователя


def handle_uploaded_files(red_files: MultiValueDict, user_id):
    names = []
    # Сохраняем загруженные файлы
    for key in red_files:
        files_list = red_files.getlist(key)
        for file in files_list:
            name = handle_uploaded_file(file, user_id)
            names.append(name)
    return names


def handle_uploaded_file(f: UploadedFile, user_id):

    # Экземпляр FileSystemStorage
    fs = FileSystemStorage('fileStore/'+user_id+"/files")

    # Получаем доступное имя файла
    name = fs.get_available_name(f.name)

    # Записываем файл
    with fs.open(name, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return name
