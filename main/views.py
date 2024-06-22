from django.shortcuts import render
import csv
from pathlib import Path
from .models import Article, QuestionResponse
from django.db.models import Q

import openai

openai.api_key = ''
LANGUE = ['fr','en']
FILE_BASE = 'main/data_txt'

def error404(request):
    """_summary_
        Affiche la page d'erreur lorsque l'utilisateur essaye charger la page avec une langue qui n'est pas spécifier dans notre application
    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    file_path = 'main/data_txt/error/content_en.csv'
    data = readCSV(file_path)
    return render(request, '404.html', data)


def check_request(ln,file_path):
    """_summary_
        Permet de vérifier si la langue séléctionné existe.
        Si la langue sélectionné existe, envoie les données à chargé de la page grâce à la méthode readCSV()
        Sinon return 'error' qui permettra d'afficher une page d'erreur.
    Args:
        ln (_type_): _description_ Choix de la langue pour la génération de la page
        file_path (_type_): _description_ Chemin du fichier csv à lire

    Returns:
        _type_: _description_ Dictionaire avec le contenu de la page (voir readCSV pour plus de détails) si la langue sélectionné existe, sinon un str 'error'
    """
    data = {}
    
    # Le navigateur envoi une requête de 'favicon.io' après le chargement
    if ln == 'favicon.ico' :
        pass
    elif ln in LANGUE:
        data=readCSV(file_path)
        file_path_base = 'main/data_txt/base/entete_'+ln+'.csv'
        data=readCSV(file_path_base,data)
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
    file_path = 'main/data_txt/home/home_'+ln+'.csv'
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


def question(request,ln):
    """_summary_
        En cours développement
        Permet l'envoi d'une question à un chatbot
    Args:
        request (_type_): _description_
        ln (_type_): _description_ Langue souhaité pour la génération de la page

    Returns:
        _type_: _description_ Page web question.html avec la réponse du chatbot
    """
    file_path = 'main/data_txt/question/page/question_'+ln+".csv"
    data = check_request(ln,file_path)

    file_path_question_response = FILE_BASE+'/question/question_response/'+ln
    path = Path(file_path_question_response)
    for file in path.rglob('*'):
        if file.is_file():
            data_question_response = readCSV(file)
            # Si l'article ne se trouve pas dans la base de donnés, une insertion s'effectue
            if len(QuestionResponse.objects.filter(question=data_question_response['question_user']))==0:
                nouvel_question_response = QuestionResponse.objects.create(question=data_question_response['question_user'], response=data_question_response['response_bot'],lang=ln)
                nouvel_question_response.save()

    data['questions'] = QuestionResponse.objects.filter(lang=ln)
    print(data['questions'])
    '''data['form'] = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['text']
            response = ask_openai(question)
            print(response)
    '''       

    return render(request, 'question.html', data)


def article(request,ln,inId):
    """_summary_
        Page de l'article sélectionné depuis la page blog
        Il sera traduit en la langue choisi
    Args:
        request (_type_): _description_
        ln (_type_): _description_ choix de la langue
        inTitle (_type_): _description_ Id de l'article choisi

    Returns:
        _type_: _description_ Page Web article.html
    """
    file_path_base = 'main/data_txt/base/entete_'+ln+'.csv'
    data=readCSV(file_path_base)
    try:
        article = Article.objects.get(id=inId)
        
        data['article'] = article
        data['ln'] = ln
    except:
        file_path = "main/data_txt/error/data_"+ln+".csv"
        data = readCSV(file_path,data)
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

    #Lecture du fichier csv et ajoute les clefs/valeurs dans un dictionnaire
    #Ses clefs permettrons d'afficher les textes correspondants dans la page html
    file_path = 'main/data_txt/blog/blog_'+ln+'.csv'
    data = check_request(ln,file_path)
    if data == 'error':
        return error404(request)
   
    # Parcour les fichiers qui se trouvent dans le répertoire de la langue sélectionné
    files_path_article = 'main/data_txt/article/'+ln
    path = Path(files_path_article)
    for file in path.rglob('*'):
        if file.is_file():
            # Récupère les données du/des csv en les stockant dans un dictionnaire
            data_article = readCSV(file)
            
            # Si l'article ne se trouve pas dans la base de donnés, une insertion s'effectue
            if len(Article.objects.filter(title=data_article['title_article']))==0:
                nouvel_article = Article.objects.create(title=data_article['title_article'], content=data_article['content_article'], publication_date=data_article['publication_date'])
                nouvel_article.save()
    

    # Parcourt la table Article et récupère les objects (articles) qui possède dans leurs titre la langue sélectionné
    get_title = '('+ln+')'
    data['articles'] = Article.objects.filter(Q(title__icontains=get_title))

    return render(request, 'templates/blog.html', data)

def readCSV(file_path,data={}):
    """_summary_
        Lit et insère dans un dictionnaire les données du csv
        ! Ses fichiers doivents correspondrent au partern: une ligne -> clef:valeur et doivent être séparés par un ; 
    Args:
        file_path (_type_): _description_ Chemin où se situe le csv
        data (dict, optional): _description_. Defaults to {}. Pour ajouter des clefs et valeurs dans un dictionnaire déja existant

    Returns:
        _type_: _description_ Dictionnaire avec toutes les clefs et valeurs du csv, permettant à être utilisé pour les pages web
    """

    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file,delimiter=";")
            
            for row in reader:
                key, value = row[0].strip(), row[1].strip()
                data[key] = value
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return data