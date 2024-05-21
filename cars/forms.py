from django import forms
from django.core.validators import EmailValidator

from .models import LicensePlate, Customer


class CustomerForm(forms.Form):
    email = forms.EmailField(validators=[EmailValidator()], label='Customer Email')

LicensePlateInlineFormSet = forms.inlineformset_factory(
    Customer, 
    LicensePlate, 
    extra=0, 
    can_delete=True, 
    fields=['plate_number']
)
