from django import forms


# Структура и органы упрвавления образовательной организацией (использовать как set)
class StructForm(forms.Form):
    name = forms.CharField(
        label="Наименование",
        required=True,
        widget=forms.TextInput())
    fio = forms.CharField(
        label="Фамилия, имя, отчество руководителя",
        required=False,
        widget=forms.TextInput())
    post = forms.CharField(
        label="Должность руководителя",
        required=False,
        widget=forms.TextInput())
    addressStr = forms.CharField(
        label="Место нахождения",
        required=False,
        widget=forms.TextInput())
    site = forms.CharField(
        label="Адрес официального сайта в сети \"Интернет\"",
        required=False,
        widget=forms.TextInput())
    email = forms.CharField(
        label="Адреса электронной почты",
        required=False,
        widget=forms.TextInput())

    divisionClauseDocLink = forms.FileField(label='Положение о структурном подразделении', required=True,
                                            widget=forms.FileInput(attrs={
                                                "required": "required"
                                            }))
    # filesField = forms.FileField(
    #     label='Выберите файлы',
    #     widget=forms.FileInput(
    #         attrs={
    #             'multiple': True
    #         }
    #     )
    # )


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
#               о языках, на которых осуществляется образование (обучение)
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
