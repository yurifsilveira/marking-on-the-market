class hearderCard {
    
    constructor() {
        this.heard = document.createElement('div');
        this.heard.className = 'card-header d-flex justify-content-between align-items-center';
    }

    addElement(element) {
        this.heard.appendChild(element);
    }
    
}

class headerButton {

    constructor(id = 'collapseExample') {
        this.button = document.createElement('button');
        this.button.className = 'btn btn-light';
        this.button.type = 'button';
        this.button.setAttribute('data-bs-toggle', 'collapse');
        this.button.setAttribute('data-bs-target', id);
        this.button.setAttribute('aria-expanded', 'false');
        this.button.setAttribute('aria-controls', id);
        this.button.innerHTML = '<img src="../static/img/down.svg" width="20" height="20" alt="Seta para baixo">';
    }
}
class headerTitle {

    constructor(text) {
        this.title = document.createElement('h6');
        this.title.className = 'col-8';
        this.title.textContent = text;
    }

}
