from django.shortcuts import render
import csv
from pathlib import Path
from .models import Article, MessageForm
from django.db.models import Q

import openai

openai.api_key = ''
LANGUE = ['fr','en']

def error404(request):
    file_path = 'main/data_txt/error/content_en.csv'
    data = readCSV(file_path,';')
    return render(request, '404.html', data)


def check_request(ln,file_path):
    """_summary_
        Permet de vérifier si la langue séléctionné existe.
        Si la langue sélectionné existe, envoie les données à chargé de la page grâce à la méthode readCSV()
        Sinon return 'error' qui permettra d'afficher une page d'erreur.
    Args:
        ln (_type_): _description_
        file_path (_type_): _description_

    Returns:
        _type_: _description_ Dictionaire avec le contenu de la page (voir readCSV pour plus de détails) si la langue sélectionné existe, sinon un str 'error'
    """
    data = {}
    
    # Le navigateur envoi une requête de 'favicon.io' après le chargement
    if ln == 'favicon.ico' :
        pass
    elif ln in LANGUE:
        print("test")
        data=readCSV(file_path,';')
        
        data['ln'] = ln
    else:
        data = 'error'
    return data

def home(request, ln='fr'):
    """_summary_
        Page d'accueil avec le contenu traduit celon la langue choisi
    Args:
        request (_type_): _description_
        ln (str, optional): _description_. Defaults to 'fr'. Choix de la langue de la page

    Returns:
        _type_: _description_ Page Web home.html 
    """
    print('test de ln:', ln)
    file_path = 'main/data_txt/home/home_'+ln+".csv"
    data = check_request(ln,file_path)
    if data == 'error':
        return error404(request)
    return render(request, 'home.html', data)


def ask_openai(message):
    """_summary_
        Permet de poser une question à un chatbot (chatgpt)
        Ce dernier à besoin d'une api key pour fonctionner
    Args:
        message (_type_): _description_ Question posé par l'utilisateur au chatbot

    Returns:
        _type_: _description_ str, La réponse correspondante à la question de l'utilisateur
    """
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    
    answer = response.choices[0].message.content.strip()
    return answer


def question(request):
    """_summary_
        En cours développement
        Permet l'envoi d'une question à un chatbot
    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_ Page web question.html avec la réponse du chatbot
    """
    
    data = {'form':  MessageForm()}
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['text']
            response = ask_openai(question)
            print(response)
            

    return render(request, 'question.html', data)


def article(request,ln,inTitle):
    """_summary_
        Page de l'article sélectionné depuis la page blog
        Il sera traduit en la langue choisi
    Args:
        request (_type_): _description_
        ln (_type_): _description_ choix de la langue
        inTitle (_type_): _description_ Titre de l'article choisi

    Returns:
        _type_: _description_ Page Web article.html
    """
    try:
        article = Article.objects.get(title=inTitle)
        data = {'article': article}
        data['ln'] = ln
    except:
        data = {'message': 'Erreur: article introuvable'}
    return render(request, 'article.html', data)


def blog(request, ln='fr'):
    """_summary_
        Affiche la page blog avec le contenu traduit par la langue sélectionné
    Args:
        request (_type_): _description_ 
        ln (str, optional): _description_. Defaults to 'fr'. Language choisi par l'utilisateur, par défaut en français

    Returns:
        _type_: _description_  Une page Web en lui envoyant le contenu traduit ainsi que les articles à afficher
    """

    #############################################
    #            Affichage des labels           #
    #############################################
    #Lecture du fichier csv et ajoute les clefs/valeurs dans un dictionnaire
    #Ses clefs permettrons d'afficher les textes correspondants dans la page html
    file_path = 'main/data_txt/blog/blog_'+ln+'.csv'
    data = check_request(ln,file_path)
    if data == 'error':
        return error404(request)
    #############################################
    #   Insertion des articles dans la bd       #
    #############################################

    # Parcour les fichiers qui se trouvent dans le répertoire de la langue sélectionné
    files_path_article = 'main/data_txt/article/'+ln
    path = Path(files_path_article)
    for file in path.rglob('*'):
        if file.is_file():
            # Récupère les données du/des csv en les stockant dans un dictionnaire
            data_article = readCSV(file, ';')
            
            # Si l'article ne se trouve pas dans la base de donnés, une insertion s'effectue
            if len(Article.objects.filter(title=data_article['title']))==0:
                nouvel_article = Article.objects.create(title=data_article['title'], content=data_article['content'], publication_date=data_article['publication_date'])
                nouvel_article.save()
    

    # Parcourt la table Article et récupère les objects (articles) qui possède dans leurs titre la langue sélectionné
    get_title = '('+ln+')'
    data['articles'] = Article.objects.filter(Q(title__icontains=get_title))

    return render(request, 'templates/blog.html', data)

def readCSV(file_path, delemit=','):
    """_summary_
        Lit et insère dans un dictionnaire les données du csv
        ! Ses fichiers doivents correspondrent au partern: une ligne -> clef:valeur
    Args:
        file_path (_type_): _description_ chemin où se situe le csv
        delemit (str, optional): _description_. Defaults to ','. Délimiteur entre les clefs et valeurs

    Returns:
        _type_: _description_ Dictionnaire avec toutes les clefs et valeurs du csv, permettant à être utilisé pour les pages web
    """
    data = {}
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=delemit)
            
            for row in reader:
                key, value = row[0].strip(), row[1].strip()
                data[key] = value
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return data