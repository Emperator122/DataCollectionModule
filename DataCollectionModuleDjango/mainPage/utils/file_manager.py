from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDict
from django.core.files.uploadedfile import UploadedFile
import os


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


def handle_uploaded_files(files_list, user_id):
    names = []
    for file in files_list:
        name = handle_uploaded_file(file, user_id)
        names.append(name)
    return names


def handle_uploaded_files_(red_files: MultiValueDict, user_id):
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
    fs = FileSystemStorage('fileStore/' + user_id + "/files")

    # Получаем доступное имя файла
    name = fs.get_available_name(f.name)

    # Записываем файл
    with fs.open(name, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return name