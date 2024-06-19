from django.db import models
from django import forms

class Article(models.Model):
    """_summary_
        Structure d'un article
    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    title = models.CharField(max_length=100)
    content = models.TextField()
    publication_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    """_summary_
        Permet de stocker les questions posé par l'utilisateur
    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    text = models.CharField(max_length=100)

    def __str__(self) :
        return self.text

class MessageForm(forms.ModelForm):
    """_summary_
        Formulaire permettant de posé des questions au chatbot
    Args:
        forms (_type_): _description_
    """
    class Meta:
        model = Message
        fields = ['text']