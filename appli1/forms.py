from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser,Product,Message
from django.forms import ModelForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address', 'preferences', 'imageUser')
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.TextInput(attrs={'class':'form-control'}),
            
            'phone_number':forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
            'Preferences':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.TextInput(attrs={'class':'form-control'}),
            'imageUser':forms.FileInput(attrs={'class':'form-control'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'description', 'price', 'image', 'status']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control','step':'0.01','min':'0'}),
    
            'status':forms.TextInput(attrs={'class':'form-control'}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
        }


class MessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=CustomUser.objects.none())

    class Meta:
        model = Message
        fields = ['recipient', 'content']
        widgets={
            'content':forms.Textarea(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user',None)
        super(MessageForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['recipient'].queryset=CustomUser.objects.filter(id__in=Message.objects.filter(recipient=user).values_list('sender_id',flat=True))
        """
class MessageForm(forms.ModelForm):
    
    class Meta:
        model = Message
        fields = ['recipient', 'content']
        widgets={
            'content':forms.Textarea(attrs={'class':'form-control'}),
        }
"""