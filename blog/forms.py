from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Profile, Category

class CustomUserCreationForm(UserCreationForm):
    # Username талбарыг заавал байлгах
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']
        
        # Medium шиг цэвэрхэн харагдуулахын тулд HTML class нэмж өгөх
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input-title', 
                'placeholder': 'Гарчиг бичих...'
            }),
            'category': forms.Select(attrs={
                'class': 'input-select'
            }),
            'content': forms.Textarea(attrs={
                'class': 'input-content', 
                'placeholder': 'Нийтлэлээ энд бичнэ үү...'
            }),
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']