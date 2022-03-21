from django import forms

from Baumanagement.models import Bill


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = Bill.fields()
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }