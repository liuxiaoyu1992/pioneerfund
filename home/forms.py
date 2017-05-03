from django import forms
from .models import CreditCards
from .fields import CreditCardField, ExpiryDateField

class CreditCardAddForm(forms.ModelForm):
    cnum = CreditCardField(required=True, label="Credit Card Number")
    exp_date = ExpiryDateField(required=True, label="Expiration Date")
    class Meta:
        model = CreditCards
        exclude = ["uid"]
        fields = [
            "cnum",
            "exp_date",
            "name"
        ]

        labels = {
            "cnum": "Credit Card Number",
            "exp_date": "Expiration Date",
            "name": "Name"
        }