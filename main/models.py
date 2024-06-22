from django.db import models

class Article(models.Model):
    """_summary_
        Structure d'un article
    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    title = models.CharField(max_length=250)
    content = models.TextField()
    publication_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class QuestionResponse(models.Model):
    """_summary_
        Permets la génération de responses selon une question choisie par l'utilisateur
    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    question = models.CharField(max_length=250)
    response = models.CharField(max_length=250)
    lang = models.CharField(max_length=2, choices=[('fr', 'Français'), ('en', 'English')])

    def __str__(self) :
        return self.question