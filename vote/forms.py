from django import forms


class VoteForm(forms.Form):
    name = forms.CharField(max_length = 100, min_length = 4, required=True)
    descr =  forms.CharField(max_length = 1000, min_length = 4, required=True)


class VariantForm(forms.Form):
    text1 = forms.CharField(max_length = 50, min_length = 1, required=True)
    text2 = forms.CharField(max_length = 50, min_length = 1, required=True)

class AddUserForm(forms.Form):
    name = forms.CharField(max_length=100, min_length=8, required=True)
    email = forms.EmailField(max_length=100, min_length=5,required=True)
    passw = forms.CharField(widget=forms.PasswordInput())
