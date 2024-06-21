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