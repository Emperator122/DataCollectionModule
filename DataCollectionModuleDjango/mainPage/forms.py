from django import forms
from DataCollectionModuleDjango.mainPage.models import Struct
from .widgets import ClearableMultipleFilesInput
from .widgets import MultipleFilesField
from django.contrib.auth.models import User
import DataCollectionModuleDjango.mainPage.utils.file_manager as fm


# Структура и органы упрвавления образовательной организацией (использовать как set)
class StructForm(forms.ModelForm):
    class Meta:
        model = Struct
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

    divisionClauseDocLink = MultipleFilesField(label='Положение о структурном подразделении', required=True,
                                               widget=ClearableMultipleFilesInput(attrs={
                                                   "required": "required",
                                                   "multiple": True
                                               }))

    def save(self, *args, **kwargs):
        struct: Struct = super().save(commit=False)
        user: User = kwargs.pop('user', None)
        struct.owner = user
        files = fm.handle_uploaded_files(self.cleaned_data.get("divisionClauseDocLink"), user.username)
        self.cleaned_data["divisionClauseDocLinkFileNames"] = files
        struct.save(self, *args, **kwargs)


# Основные сведения (использовать отдельно)
class CommonForm(forms.Form):
    name = forms.CharField(
        label="Наименование образовательной организации",
        required=True,
        widget=forms.TextInput())
    regDate = forms.DateField(required=True, label="Дата создания образовательной организации")
    address = forms.CharField(
        label="Адрес",
        required=True,
        widget=forms.TextInput())
    workTime = forms.CharField(required=True, widget=forms.Textarea(), label="Режим, график работы")
    telephone = forms.CharField(
        label="Контактные телефоны",
        required=True,
        widget=forms.TextInput())
    fax = forms.CharField(
        label="Факсы",
        required=True,
        widget=forms.TextInput())
    email = forms.CharField(
        label="Адреса электронной почты",
        required=True,
        widget=forms.TextInput())
    additionalInformation = forms.CharField(widget=forms.Textarea(), label="Дополнительная информация")


# Основные сведения -> Информация об учередителях (использовать как set)
class UchredLawForm(forms.Form):
    nameUchred = forms.CharField(
        label="Наименование учредителя",
        required=True,
        widget=forms.TextInput())
    fullnameUchred = forms.CharField(
        label="ФИО руководителя учредителя (учредителя)",
        required=True,
        widget=forms.TextInput())
    addressUchred = forms.CharField(
        label="Юридический адрес",
        required=True,
        widget=forms.TextInput())
    telUchred = forms.CharField(
        label="Контактные телефоны",
        required=True,
        widget=forms.TextInput())
    mailUchred = forms.CharField(
        label="Адрес электронной почты",
        required=True,
        widget=forms.TextInput())
    websiteUchred = forms.CharField(
        label="Адрес сайта учредителя в сети \"Интернет\"",
        required=True,
        widget=forms.TextInput())
    isIndividual = forms.BooleanField(label="Учредитель - физ. лицо")


# Основные сведения -> Информация об филиалах (использовать как set)
class FilInfoForm(forms.Form):
    nameFil = forms.CharField(
        label="Наименование",
        required=True,
        widget=forms.TextInput())
    addressFil = forms.CharField(
        label="Место нахождения",
        required=True,
        widget=forms.TextInput())
    workTimeFil = forms.CharField(
        label="Режим и график работы",
        required=True,
        widget=forms.TextInput())
    telephoneFil = forms.CharField(
        label="Контактные телефоны",
        required=True,
        widget=forms.TextInput())
    emailFil = forms.CharField(
        label="Адрес электронной почты",
        required=True,
        widget=forms.TextInput())
    websiteFil = forms.CharField(
        label="Адрес официального сайта в сети \"Интернет\"",
        required=True,
        widget=forms.TextInput())


# Основные сведения -> Информация о представительствах (использовать как set)
class RepInfoForm(forms.Form):
    nameRep = forms.CharField(
        label="Наименование",
        required=True,
        widget=forms.TextInput())
    addressRep = forms.CharField(
        label="Место нахождения",
        required=True,
        widget=forms.TextInput())
    workTimeRep = forms.CharField(
        label="Режим и график работы",
        required=True,
        widget=forms.TextInput())
    telephoneRep = forms.CharField(
        label="Контактные телефоны",
        required=True,
        widget=forms.TextInput())
    emailRep = forms.CharField(
        label="Адрес электронной почты",
        required=True,
        widget=forms.TextInput())
    websiteRep = forms.CharField(
        label="Адрес официального сайта в сети \"Интернет\"",
        required=True,
        widget=forms.TextInput())


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
