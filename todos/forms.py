from django.forms.widgets import TextInput, Textarea
from .models import Todo
from django import forms
from django.forms import ModelForm, models, DateInput,TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TodoForm(ModelForm):

    class Meta:
        model = Todo
        widgets = {
        'due_to': DateInput(format=('%m/%d/%Y'), 
                            attrs={'placeholder':'Select a date', 'type':'date'}),
        'title': TextInput(attrs={"placeholder":"Title"}),
        "description" : Textarea(attrs={"placeholder":"Description"}),                 
    }
        fields = ['title', 'description', 'due_to', 'isCompleted']

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user