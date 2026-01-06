class cardBody {

    constructor(containerId) {

        this.collapse = document.createElement('div');
        this.collapse.className = 'collapse';
        this.collapse.id = containerId;

        this.body = document.createElement('div');
        this.body.className = 'card-body';
        this.body.id = containerId;

        this.collapse.appendChild(this.body);
    }
    addElement(element) {
        this.body.appendChild(element);
    }
}

class bodyTitle {

    constructor(title) {
        this.title = document.createElement('h5');
        this.title.className = 'card-title';
        this.title.textContent = title;
    }

}