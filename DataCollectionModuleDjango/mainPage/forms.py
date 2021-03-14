from django import forms
from django.db import models
import DataCollectionModuleDjango.mainPage.models as pageGenModels
from .widgets import ClearableMultipleFilesInput
from .widgets import MultipleFilesField
from django.contrib.auth.models import User
import DataCollectionModuleDjango.mainPage.utils.file_manager as fm
from django.core.files.uploadedfile import UploadedFile


# Модель с переписанным save для наследования от нее
class OwnedModelForm(forms.ModelForm):
    # Окончание идентефикатора поля в модели, соотвествующего полю загрузки из формы
    # (т.е. если поле загрузки на форме divisionClauseDocLink, то JSON поле в модели
    # будет именовиться divisionClauseDocLink+file_names_suffix (divisionClauseDocLinkFileNames)
    file_names_suffix = "FileNames"

    def save(self, *args, **kwargs):
        model_obj = super().save(commit=False)  # получаем почти заполненный экземпляр модели (без эксклудов)
        # заполняем поле "owner" переданным пользователем
        user: User = kwargs.pop('user', None)
        model_obj.owner = user
        # загружаем данные на серв и заполняем JSON поле модели
        for key, item in self.cleaned_data.items():
            if isinstance(item, list) and any(isinstance(i, UploadedFile) for i in item):  # если item - list файлов
                files = fm.handle_uploaded_files(item, user.username)  # загружаем файлы на серв
                model_field_name = key + self.file_names_suffix
                if hasattr(model_obj, model_field_name):  # если модель имеет необходимое поле, то заполняем его
                    self.cleaned_data[model_field_name] = files  # и редачим чистые данные
                    setattr(model_obj, model_field_name, files)

        # Определяемся следует ли коммитить
        commit_arg = kwargs.pop("commit", None)
        if commit_arg is not None and not commit_arg:
            return model_obj
        model_obj.save(self)
        return model_obj

    @staticmethod  # вернет формсет из форм
    def get_formset_class(model, form):
        return forms.modelformset_factory(model=model, form=form, extra=0, min_num=1)

    @staticmethod  # вернет формсет из форм принадлежащих юзеру, либо сет из одной формы
    def get_owned_formset(user: User, model, form, **kwargs):
        objects = kwargs.pop('owner', None)
        if objects is None:
            objects = model.objects.filter(owner=user)
        formset = OwnedModelForm.get_formset_class(model, form)
        return formset(queryset=objects, **kwargs)


# Структура и органы упрвавления образовательной организацией (использовать как set)
class StructForm(OwnedModelForm):
    class Meta:
        model = pageGenModels.Struct
        exclude = ['owner']
        labels = {
            "name": "Наименование",
            "fio": "Фамилия, имя, отчество руководителя",
            "post": "Должность руководителя",
            "addressStr": "Место нахождения",
            "site": "Адрес официального сайта в сети \"Интернет\"",
            "email": "Адреса электронной почты",
            "divisionClauseDocLink": "Положение о структурном подразделении"
        }

    divisionClauseDocLink = MultipleFilesField(label='Положение о структурном подразделении', required=False,
                                               widget=ClearableMultipleFilesInput(attrs={
                                                   "multiple": True
                                               }))


# Основные сведения (использовать отдельно)
class CommonForm(OwnedModelForm):
    class Meta:
        model = pageGenModels.Common
        exclude = ['owner']
        labels = {
            "name": "Наименование образовательной организации",
            "regDate": "Дата создания образовательной организации",
            "address": "Адрес",
            "workTime": "Режим, график работы",
            "telephone": "Контактные телефоны",
            "fax": "Факсы",
            "email": "Адреса электронной почты",
            "additionalInformation": "Дополнительная информация"
        }
        widgets = {
            "workTime": forms.Textarea(),
            "additionalInformation": forms.Textarea(),
            "regDate": forms.DateInput(attrs={'class': 'form-control', "type": "date"}, format='%Y-%m-%d')
        }


# Основные сведения -> Информация об учередителях (использовать как set)
class UchredLawForm(OwnedModelForm):
    class Meta:
        model = pageGenModels.UchredLaw
        exclude = ['owner']
        labels = {
            "nameUchred": "Наименование учредителя",
            "fullnameUchred": "ФИО руководителя (учредителя)",
            "addressUchred": "Юридический адрес",
            "telUchred": "Контактные телефоны",
            "mailUchred": "Адрес электронной почты",
            "websiteUchred": "Адрес сайта учредителя в сети \"Интернет\"",
            "isIndividual": "Учредитель - физ. лицо"
        }


# Основные сведения -> Информация о филиалах (использовать как set)
class FilInfoForm(OwnedModelForm):
    class Meta:
        model = pageGenModels.FilInfo
        exclude = ['owner']
        labels = {
            "nameFil": "Наименование",
            "addressFil": "Место нахождения",
            "workTimeFil": "Режим и график работы",
            "telephoneFil": "Контактные телефоны",
            "emailFil": "Адрес электронной почты",
            "websiteFil": "Адрес официального сайта в сети \"Интернет\""
        }


# Основные сведения -> Информация о представительствах (использовать как set)
class RepInfoForm(OwnedModelForm):
    class Meta:
        model = pageGenModels.RepInfo
        exclude = ['owner']
        labels = {
            "nameRep": "Наименование",
            "addressRep": "Место нахождения",
            "workTimeRep": "Режим и график работы",
            "telephoneRep": "Контактные телефоны",
            "emailRep": "Адрес электронной почты",
            "websiteRep": "Адрес официального сайта в сети \"Интернет\""
        }


#
# ОПИСАННЫЕ НИЖЕ ФОРМЫ НЕОБХОДИМО ПРИВЕСТИ К MODELFORM
#
# Обазование ->
#               Информация о сроке действия государственной аккредитации образовательной программы,
#               о языках, на которых осуществляется образование (обучение) (set)
class EduAccredForm(forms.Form):
    eduCode = forms.CharField(
        label="Код специальности, направления подготовки",
        required=True,
        widget=forms.TextInput())
    eduName = forms.CharField(
        label="Наименование",
        required=True,
        widget=forms.TextInput())
    eduLevel = forms.CharField(
        label="Уровень образования",
        required=True,
        widget=forms.TextInput())
    eduForm = forms.CharField(
        label="Форма обучения",
        required=True,
        widget=forms.TextInput())
    learningTerm = forms.CharField(
        label="Нормативный срок обучения",
        required=True,
        widget=forms.TextInput())
    dateEnd = forms.CharField(
        label="Срок действия государственной аккредитации",
        required=True,
        widget=forms.TextInput())
    language = forms.CharField(
        label="Языки, на которых осуществляется образование",
        required=True,
        widget=forms.TextInput())


# Обазование -> Информация по образовательным программам (set)
class EduOpForm(forms.Form):
    eduCode = forms.CharField(
        label="Код специальности, направления подготовки",
        required=True,
        widget=forms.TextInput())
    eduName = forms.CharField(
        label="Наименование",
        required=True,
        widget=forms.TextInput())
    eduLevel = forms.CharField(
        label="Уровень образования",
        required=True,
        widget=forms.TextInput())
    eduForm = forms.CharField(
        label="Форма обучения",
        required=True,
        widget=forms.TextInput())
    opMain = forms.FileField(
        label="Ссылка на описание образовательной программы с приложением ее копии",
        widget=forms.FileInput(
            attrs={
                'multiple': True
            }
        )
    )
    educationPlan = forms.FileField(
        label="Ссылка на учебный план",
        widget=forms.FileInput(
            attrs={
                'multiple': True
            }
        )
    )
    educationAnnotation = forms.FileField(
        label="Ссылки на аннотации к рабочим программам дисциплин (по каждой дисциплине в составе образовательной "
              "программы)",
        widget=forms.FileInput(
            attrs={
                'multiple': True
            }
        )
    )
    educationShedule = forms.FileField(
        label="Ссылка на календарный учебный график",
        widget=forms.FileInput(
            attrs={
                'multiple': True
            }
        )
    )
    methodology = forms.FileField(
        label="Ссылка на методические и иные документы, разработанные образовательной организацией для обеспечения "
              "образовательного процесса",
        widget=forms.FileInput(
            attrs={
                'multiple': True
            }
        )
    )
    eduPr = forms.FileField(
        label="Ссылка на рабочие программы практик, предусмотренных соответствующей образовательной программой",
        widget=forms.FileInput(
            attrs={
                'multiple': True
            }
        )
    )
    eduEl = forms.FileField(
        label="Использование при реализации образовательных программ электронного обучения и дистанционных "
              "образовательных технологий",
        widget=forms.FileInput(
            attrs={
                'multiple': True
            }
        )
    )
    isAdapted = forms.BooleanField(label="Адаптированная программа")


# Образование -> Информация о численности обучающихся за счет бюджетных ассигнований федерального бюджета,
# бюджетов субъектов Российской Федерации, местных бюджетов, по договорам об образовании за счет средств физических и
# (или) юридических лиц (set)
class EduChislenForm(forms.Form):
    eduCode = forms.CharField(
        label="Код специальности, направления подготовки",
        required=True,
        widget=forms.TextInput())
    eduName = forms.CharField(
        label="Наименование профессии, специальности, направления подготовки",
        required=True,
        widget=forms.TextInput())
    eduLevel = forms.CharField(
        label="Уровень образования",
        required=True,
        widget=forms.TextInput())
    eduForm = forms.CharField(
        label="Форма обучения",
        required=True,
        widget=forms.TextInput())
    numberBFpriem = forms.CharField(
        label="бюджетных ассигнований федерального бюджета ",
        required=True,
        widget=forms.TextInput())
    # Численность обучающихся за счет (количество человек)
    numberBRpriem = forms.CharField(
        label="бюджетов субъектов Российской Федерации",
        required=True,
        widget=forms.TextInput())
    numberBMpriem = forms.CharField(
        label="местных бюджетов",
        required=True,
        widget=forms.TextInput())
    numberPpriem = forms.CharField(
        label="средств физических и (или) юридических лиц",
        required=True,
        widget=forms.TextInput())
    numberF = forms.CharField(
        label="Численность обучающихся, являющихся иностранными гражданами",
        required=True,
        widget=forms.TextInput())
