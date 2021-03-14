import os
from django.contrib.auth.models import User
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.forms.models import BaseModelFormSet
import DataCollectionModuleDjango.mainPage.models as pg_models
import DataCollectionModuleDjango.mainPage.forms as pg_forms


# Базовый класс, от которого будут наследоваться все остальные генераторы
# при должно оформлении именно он дает им основной функционал
class BasePageGenerator(object):
    user = None
    data = None
    files = None
    DirName = "sampleDirname"  # необходимо преопределить
    renderPath = "sample/path/to/file.html"

    __isValid__ = None

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

    def __init__(self, user, data=None, files=None):
        self.user = user
        self.files = files
        self.data = data

        for setting in self.FormsetsAttrsSettings:
            class_name = setting['FormsetClassName']
            form_link = setting['FormsetForm']
            model_link = setting['FormsetModel']
            setattr(self, class_name, form_link.get_formset_class(model_link, form_link))

    def get_rendered_html(self) -> str:
        if not self.validate_formsets():
            return "<b>Ошибка генерации файла: ошибка при валидации форм</b>"

        context = {}
        for setting in self.FormsetsAttrsSettings:
            obj_name = setting['FormsetObjectName']
            context[obj_name] = getattr(self, obj_name, None)
            if context[obj_name] is None:
                return "Ошибка генерации файла: один из формсетов - None"

        return render_to_string(self.renderPath, context=context)

    def save_html(self, encoding='utf-8'):
        html = self.get_rendered_html()  # получаем html
        fs = FileSystemStorage(os.path.join("fileStore/", self.user.username))  # заходим в хранилище пользователя
        path_to_dir = os.path.join(fs.location, self.DirName)

        if not os.path.exists(path_to_dir):
            os.mkdir(os.path.join(fs.location, self.DirName))  # создаем папку для index.html

        with fs.open(os.path.join(path_to_dir, "index.html"), 'wb') as destination:  # сохраняем файл index.html
            destination.write(html.encode(encoding))

    def get_user_formsets(self, rewrite=True):
        formsets = []
        for setting in self.FormsetsAttrsSettings:
            obj_name = setting['FormsetObjectName']  # Получаем свойства
            form_link = setting['FormsetForm']
            model_link = setting['FormsetModel']
            prefix = setting['prefix']
            # создаем формсеты и добавляем их в лист
            formset_obj = form_link.get_owned_formset(self.user, model_link, form_link, prefix=prefix)
            formsets.append(formset_obj)
            if rewrite:
                setattr(self, obj_name, formset_obj)
                self.__isValid__ = None

        return tuple(formsets)

    def get_formsets_from_data(self, rewrite=True):
        formsets = []
        for setting in self.FormsetsAttrsSettings:
            class_name = setting['FormsetClassName']
            obj_name = setting['FormsetObjectName']  # Получаем свойства
            prefix = setting['prefix']
            # получаем экземпляр класса, создаем объект и вкидываем его в лист
            formset_class = getattr(self, class_name)
            formset_obj = formset_class(data=self.data, files=self.files, prefix=prefix)
            formsets.append(formset_obj)
            if rewrite:
                setattr(self, obj_name, formset_obj)
                self.__isValid__ = None

        return tuple(formsets)

    def validate_formsets(self) -> bool:
        if self.__isValid__ is not None:
            return self.__isValid__
        self.__isValid__ = True

        for setting in self.FormsetsAttrsSettings:
            obj_name = setting['FormsetObjectName']
            formset_object = getattr(self, obj_name)
            self.__isValid__ = self.__isValid__ and formset_object.is_valid()

        return self.__isValid__

    def save_formsets(self):
        if self.validate_formsets():
            for setting in self.FormsetsAttrsSettings:
                obj_name = setting['FormsetObjectName']
                formset_object = getattr(self, obj_name)
                for form in formset_object:
                    form.save(user=self.user)

    def delete_db_data(self):
        result = False
        if self.data is not None and self.validate_formsets():
            result = True
            for setting in self.FormsetsAttrsSettings:
                obj_name = setting['FormsetObjectName']
                formset_object = getattr(self, obj_name)
                formset_object.get_queryset().delete()
        return result


class StructPageGenerator(BasePageGenerator):
    DirName = "struct"
    renderPath = "pageGenerator/struct.html"
    FormsetsAttrsSettings = [
        {
            'prefix': 'struct',
            'FormsetClassName': 'StructFormset',
            'FormsetObjectName': 'structFormsetObj',
            'FormsetModel': pg_models.Struct,
            'FormsetForm': pg_forms.StructForm,
        }
    ]
    StructFormset = None
    structFormsetObj = None


class CommonPageGenerator(BasePageGenerator):
    DirName = "common"
    renderPath = "pageGenerator/common.html"
    FormsetsAttrsSettings = [
        {
            'prefix': 'common',
            'FormsetClassName': 'CommonFormset',
            'FormsetObjectName': 'commonFormsetObj',
            'FormsetModel': pg_models.Common,
            'FormsetForm': pg_forms.CommonForm,
        },
        {
            'prefix': 'uchred_law',
            'FormsetClassName': 'UchredLawFormset',
            'FormsetObjectName': 'uchredLawFormsetObj',
            'FormsetModel': pg_models.UchredLaw,
            'FormsetForm': pg_forms.UchredLawForm,
        },
        {
            'prefix': 'fil_info',
            'FormsetClassName': 'FilInfoFormset',
            'FormsetObjectName': 'filInfoFormsetObj',
            'FormsetModel': pg_models.FilInfo,
            'FormsetForm': pg_forms.FilInfoForm,
        },
        {
            'prefix': 'rep_info',
            'FormsetClassName': 'RepInfoFormset',
            'FormsetObjectName': 'repInfoFormsetObj',
            'FormsetModel': pg_models.RepInfo,
            'FormsetForm': pg_forms.RepInfoForm,
        }
    ]
    CommonFormset = None
    commonFormsetObj = None
    UchredLawFormset = None
    uchredLawFormsetObj = None
    FilInfoFormset = None
    filInfoFormsetObj = None
    RepInfoFormset = None
    repInfoFormsetObj = None
