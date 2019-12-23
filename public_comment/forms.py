import bootstrap_datepicker_plus as datetimepicker
from django import forms
from public_comment.models import Comment
from django.core.mail import BadHeaderError, send_mail

class DetailSearch(forms.Form):
    title = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': "キーワード",
        }),
        required=False,
    )
    


    
    
