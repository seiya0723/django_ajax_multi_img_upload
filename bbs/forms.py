from django import forms
from .models import Topic,TopicImage

class TopicForm(forms.ModelForm):

    class Meta:
        model   = Topic
        fields  = [ "comment" ]

class TopicImageForm(forms.ModelForm):

    class Meta:
        model   = TopicImage
        fields  = [ "topic","image" ]


