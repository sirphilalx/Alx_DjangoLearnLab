from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import Post
from .models import Comment


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        super(PostForm, self).__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super().clean()
        if self.author:
            cleaned_data['author'] = self.author
        return cleaned_data
    

# Comment form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your comment here...'}),
        }

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        self.post = kwargs.pop('post', None)
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        if content:
            if len(content) < 10:
                raise forms.ValidationError("Comment must be at least 10 characters long.")
        return cleaned_data

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.author = self.author
        comment.post = self.post
        if commit:
            comment.save()
        return comment