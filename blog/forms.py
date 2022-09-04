from .models import Comment, Post
from django import forms
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
        widgets = {
            'comment':forms.Textarea()
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','slug','body','status','tags']
        widgets = {
            'body':CKEditorWidget(),
        }



