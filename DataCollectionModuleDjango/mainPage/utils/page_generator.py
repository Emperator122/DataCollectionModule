import os
from django.contrib.auth.models import User
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.forms.models import BaseModelFormSet
import DataCollectionModuleDjango.mainPage.models as pg_models
import DataCollectionModuleDjango.mainPage.forms as pg_forms


class BasePageGenerator(object):
    user = None
    data = None
    files = None
    DirName = "sampleDirname"  # необходимо преопределить

    # Массив характеристик каждого формсета. Должен быть переопределен. Данный для примера
    FormsetsAttrsSettings = [
        {
            'prefix': 'sample_prefix',
            'FormsetClassName': 'SampleClassName',
            'FormsetObjectName': 'sampleObjectName',
            'FormsetModel': models.Model,
            'FormsetForm': pg_forms.OwnedModelForm,
        },
        {
            'prefix': 'sample_prefix2',
            'FormsetClassName': 'SampleClassName2',
            'FormsetObjectName': 'sampleObjectName2',
            'FormsetModel': models.Model,
            'FormsetForm': pg_forms.OwnedModelForm,
        },
    ]


class StructPageGenerator(object):
    user = None
    data = None
    files = None
    DirName = "struct"

    StructFormsetPrefix = "struct"
    StructFormset = pg_forms.StructForm.get_formset_class(pg_models.Struct, pg_forms.StructForm)

    structFormsetObj = None
    __isValid__ = None

    def __init__(self, user, data=None, files=None):
        self.user = user
        self.files = files
        self.data = data

    def get_rendered_html(self) -> str:
        if self.structFormsetObj is None:
            return "<b>Ошибка генерации файла: formset - null</b>"
        if not self.validate_formsets():
            return "<b>Ошибка генерации файла: ошибка при валидации форм</b>"

        return render_to_string("pageGenerator/struct.html", context={"structOrgUprav_formset": self.structFormsetObj})

    def save_html(self, encoding='utf-8'):
        html = self.get_rendered_html()  # получаем html
        fs = FileSystemStorage(os.path.join("fileStore/", self.user.username))  # создаем необходимую папку
        path_to_dir = os.path.join(fs.location, self.DirName)

        if not os.path.exists(path_to_dir):
            os.mkdir(os.path.join(fs.location, self.DirName))

        with fs.open(os.path.join(path_to_dir, "index.html"), 'wb') as destination:  # сохраняем файл
            destination.write(html.encode(encoding))

    def get_user_formsets(self, rewrite=True):
        struct_formset_obj = pg_forms.StructForm.get_owned_formset(self.user, pg_models.Struct, pg_forms.StructForm,
                                                                   prefix=self.StructFormsetPrefix)
        if rewrite:
            self.structFormsetObj = struct_formset_obj
            self.__isValid__ = None

        return self.structFormsetObj

    def get_formsets_from_data(self, rewrite=True):
        struct_formset_obj = self.StructFormset(data=self.data, files=self.files, prefix=self.StructFormsetPrefix)

        if rewrite:
            self.structFormsetObj = struct_formset_obj
            self.__isValid__ = None

        return self.structFormsetObj

    def validate_formsets(self) -> bool:
        if self.__isValid__ is not None:
            return self.__isValid__
        self.__isValid__ = True
        self.__isValid__ = self.__isValid__ and self.structFormsetObj.is_valid()
        return self.__isValid__

    def save_formsets(self):
        if self.validate_formsets():
            for form in self.structFormsetObj:
                form.save(user=self.user)




class CommonPageGenerator(object):
    common_formset: BaseModelFormSet
    uchred_law_formset: BaseModelFormSet
    fil_info_formset: BaseModelFormSet
    rep_info_formset: BaseModelFormSet
    dir_name = "common"
