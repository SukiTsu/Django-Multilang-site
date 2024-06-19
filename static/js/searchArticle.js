// Permet de rendre fonctionnel le input text servant à la recherche d'un article
// Cache tout les autre articles qui ne possède pas le contenu entré
document.getElementById('searchBar').addEventListener('input', function() {
    // Récupère la valeur de la barre de recherche
    let filter = this.value.toLowerCase();
    
    // Récupère les articles
    let articles = document.querySelectorAll('#articleList .article');
    
    // Parcourt tous les articles et cache ceux qui ne correspondent pas à la recherche
    articles.forEach(function(article) {
      let text = article.textContent.toLowerCase();
      if (text.includes(filter)) {
        article.style.display = '';
      } else {
        article.style.display = 'none';
      }
    });
  });
  