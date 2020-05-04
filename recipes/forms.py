from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Grocery, Recipe, Contact
from django.forms import modelformset_factory
from django.forms.models import inlineformset_factory


# Sign Up Form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class ReceipeForm(ModelForm):
    class Meta:
        model = Grocery
        fields = '__all__'


class GroceryModelForm(ModelForm):
    class Meta:
        model = Grocery
        fields = ('content', 'user')


GroceryModelFormSet = inlineformset_factory(Recipe, Grocery, form=GroceryModelForm, extra=2)
# Used GroceryModelFormset for dynamid (add/delete) multiple GroceryForm.
