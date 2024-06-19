// Rend fonctionnel le selectbox pour changer la langue de la page
// Récupère le chemin actuel, change la langue actuel qui se trouve entre /--/ et la remplace par celle sélectionné
document.addEventListener('DOMContentLoaded', function(){
    const selectBox = document.getElementById('select');

    if (selectBox){
        selectBox.addEventListener('change', function(){
            const selectValue = selectBox.value;
            var currentUrl = window.location.href;

            // Obtient l'emplacement de la langue dans le chemin
            var regex = /\/([^\/]{2})\//;

            // Met à jour la langue avec celle selectionné
            var newUrl = currentUrl.replace(regex, '/'+selectValue+'/');
            // Redirige l'utilisateur à la page correspondante
            window.location.href = newUrl;
        })
    }
})