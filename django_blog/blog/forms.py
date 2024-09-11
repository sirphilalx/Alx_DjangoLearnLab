from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import Post, Comment, Tag


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

    # tags = forms.ModelMultipleChoiceField(
    #     queryset=Tag.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=False
    # )
    tags = forms.CharField(required=False, help_text="Enter tags separated by commas")


    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        
    # def __init__(self, *args, **kwargs):
    #     self.author = kwargs.pop('author', None)
    #     super(PostForm, self).__init__(*args, **kwargs)
        
    # def clean(self):
    #     cleaned_data = super().clean()
    #     if self.author:
    #         cleaned_data['author'] = self.author
    #     return cleaned_data
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tags'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])

    def save(self, commit=True):
        instance = super(PostForm, self).save(commit=False)
        
        if commit:
            instance.save()

            # TagWidget()

        # Clear existing tags
        instance.tags.clear()

        # Add new tags
        tag_names = [name.strip() for name in self.cleaned_data['tags'].split(',') if name.strip()]
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            instance.tags.add(tag)

        return instance
    

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