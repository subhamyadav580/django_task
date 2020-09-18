from django import forms
from .models import User
from django.contrib.auth import authenticate
import string 
import random 


def random_key(length):
	key = ''
	for i in range(length):
		key += random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
	return key




class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', min_length=8 ,widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', min_length=8 ,widget=forms.PasswordInput)
    uniqueID = forms.CharField(label='uniqueID', max_length=6 ,min_length=6,widget=forms.TextInput(), required=False)

    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'age', 'picture', 'uniqueID', 'password1', 'password2')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        uniqueID = self.cleaned_data.get("uniqueID")
        if uniqueID:
            uniqueID_length = len(uniqueID)
            if uniqueID_length == 6 and uniqueID.isalnum():
                user.uniqueID = uniqueID
            else:
                raise forms.ValidationError("Unique id is not alphanumeric or not of length 6")
        else:
            uniqueID = random_key(6)
            user.uniqueID = uniqueID
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'password')
    #it will check weather the credentials are true or not

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")

