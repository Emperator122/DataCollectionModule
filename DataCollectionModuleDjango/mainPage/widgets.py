from django.forms.widgets import ClearableFileInput
from django.forms.widgets import CheckboxInput
from django.forms.fields import FileField
from django.core.exceptions import ValidationError


FILE_INPUT_CONTRADICTION = object()


class ClearableMultipleFilesInput(ClearableFileInput):
    def value_from_datadict(self, data, files, name):
        upload = files.getlist(name) # files.get(name) in Django source

        if not self.is_required and CheckboxInput().value_from_datadict(
                data, files, self.clear_checkbox_name(name)):

            if upload:
                # If the user contradicts themselves (uploads a new file AND
                # checks the "clear" checkbox), we return a unique marker
                # objects that FileField will turn into a ValidationError.
                return FILE_INPUT_CONTRADICTION
            # False signals to clear any existing value, as opposed to just None
            return False
        return upload


class MultipleFilesField(FileField):
    widget = ClearableMultipleFilesInput

    def clean(self, data, initial=None):
        # If the widget got contradictory inputs, we raise a validation error
        if data is FILE_INPUT_CONTRADICTION:
            raise ValidationError(self.error_message['contradiction'], code='contradiction')
        # False means the field value should be cleared; further validation is
        # not needed.
        if data is False:
            if not self.required:
                return False
            # If the field is required, clearing is not possible (the widg    et
            # shouldn't return False data in that case anyway). False is not
            # in self.empty_value; if a False value makes it this far
            # it should be validated from here on out as None (so it will be
            # caught by the required check).
            data = None
        if not data and initial:
            return initial
        return data