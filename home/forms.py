from django import forms
from .models import CreditCards, Pledges
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
            "cnum": "Credit card Number",
            "exp_date": "Expiration date",
            "name": "Name"
        }

class PledgeAddForm(forms.ModelForm):
    class Meta:
        model = Pledges
        exclude = ['uid', 'pid']
        fields = [
            "amount",
            "cnum"
        ]
        labels = {
            "amount": "Pledge amount",
            "cnum": "Credit card number",
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PledgeAddForm, self).__init__(*args, **kwargs)
        self.fields['cnum'].queryset = CreditCards.objects.filter(uid_id=user.id)