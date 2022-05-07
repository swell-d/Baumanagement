from django.forms import TextInput, forms


class EmptyForm(forms.Form):
    base_fields = 'base',


class ColorFieldWidget(TextInput):
    input_type = 'color'
