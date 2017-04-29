from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser


# User = get_user_model()
#
# # class CustomUserCreationForm(UserCreationForm):
# #     class Meta(UserCreationForm):
# #         model = CustomUser
# #         fields = UserCreationForm.Meta.fields + ('address', 'city', 'state', 'country', 'interests')
#
# # class UserCreationForm(forms.ModelForm):
# #     """
# #     A form that creates a user, with no privileges, from the given username and
# #     password.
# #     """
# #     error_messages = {
# #         'duplicate_username': "A user with that username already exists.",
# #         'password_mismatch': "The two password fields didn't match.",
# #         }
# #     username = forms.RegexField(label="Username", max_length=30,
# #         regex=r'^[\w.@+-]+$',
# #         help_text="Required. 30 characters or fewer. Letters, digits and "
# #                     "@/./+/-/_ only.",
# #         error_messages={
# #             'invalid': ("This value may contain only letters, numbers and "
# #                          "@/./+/-/_ characters.")})
# #     password1 = forms.CharField(label=("Password"),
# #         widget=forms.PasswordInput)
# #     password2 = forms.CharField(label="Password confirmation",
# #         widget=forms.PasswordInput,
# #         help_text="Enter the same password as above, for verification.")
# #
# #     class Meta:
# #         model = CustomUser
# #         fields = ('username','password1','password2','email','user_type','token','username1','username2','username3','username4','username5',)
# #
# #     def clean_username(self):
# #         # Since User.username is unique, this check is redundant,
# #         # but it sets a nicer error message than the ORM. See #13147.
# #         username = self.cleaned_data["username"]
# #         try:
# #             CustomUser.objects.get(username=username)
# #         except CustomUser.DoesNotExist:
# #             return username
# #         raise forms.ValidationError(self.error_messages['duplicate_username'])
# #
# #     def clean_password2(self):
# #         password1 = self.cleaned_data.get("password1")
# #         password2 = self.cleaned_data.get("password2")
# #         if password1 and password2 and password1 != password2:
# #             raise forms.ValidationError(
# #                 self.error_messages['password_mismatch'])
# #         return password2
# #
# #     def save(self, commit=True):
# #         user = super(UserCreationForm, self).save(commit=False)
# #         user.set_password(self.cleaned_data["password1"])
# #         if commit:
# #             user.save()
# #         return user
#

#
#
