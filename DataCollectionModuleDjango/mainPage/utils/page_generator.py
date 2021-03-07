import os
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.forms.models import BaseModelFormSet
from DataCollectionModuleDjango.mainPage.forms import StructForm


class StructPageGenerator(object):
    structFormset: BaseModelFormSet
    dir_name = "struct"

    def __init__(self, struct_formset):
        self.structFormset = struct_formset

    def get_rendered_html(self) -> str:
        return render_to_string("pageGenerator/struct.html", context={"structOrgUprav_formset": self.structFormset})

    def save_html(self, user: User, encoding='utf-8'):
        html = self.get_rendered_html()  # получаем html
        fs = FileSystemStorage("fileStore/" + user.username)  # создаем необходимую папку
        path_to_dir = os.path.join(fs.location, self.dir_name)

        if not os.path.exists(path_to_dir):
            os.mkdir(os.path.join(fs.location, self.dir_name))

        with fs.open(os.path.join(path_to_dir, "index.html"), 'wb') as destination:  # сохраняем файл
            destination.write(html.encode(encoding))
