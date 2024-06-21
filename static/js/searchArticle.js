document.getElementById('searchBar').addEventListener('input', function() {
    // Récupère la valeur de la barre de recherche
    let filter = this.value.toLowerCase();

    // Récupère les articles
    let articles = document.querySelectorAll('#articleList .article');

    // Parcourt tous les articles et cache ceux qui ne correspondent pas à la recherche
    articles.forEach(function(article) {
        let content = article.querySelector('.content');
        let title = article.querySelector('.title');
        let text = content.textContent.toLowerCase();

        // Réinitialise le contenu pour enlever les surlignages précédents
        content.innerHTML = content.textContent;

        if (text.includes(filter)) {
            article.style.display = '';
            highlightText(content, filter);
            // Affiche le contenu et tourne la flèche si les mots recherchés apparaissent
            content.style.display = 'block';
            title.classList.add('open');
            title.querySelector('.arrow').style.transform = 'rotate(90deg)';
        } else {
            // Cache l'article
            article.style.display = 'none';
            // Cache le contenu et réinitialise la flèche
            content.style.display = 'none';
            title.classList.remove('open');
            title.querySelector('.arrow').style.transform = 'rotate(0deg)';
        }
    });
});

function highlightText(element, query) {
    let text = element.innerHTML;
    let regex = new RegExp(`(${query})`, 'gi');
    let highlightedText = text.replace(regex, '<span class="highlight">$1</span>');
    element.innerHTML = highlightedText;
}

function toggleContent(element) {
    var content = element.nextElementSibling;
    var arrow = element.querySelector('.arrow');

    if (content.style.display === "block") {
        content.style.display = "none";
        arrow.style.transform = "rotate(0deg)";
    } else {
        content.style.display = "block";
        arrow.style.transform = "rotate(90deg)";
    }

    element.classList.toggle('open');
}
