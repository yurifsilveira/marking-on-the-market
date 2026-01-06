class card {

    constructor(title) {

        this.card = document.createElement('div');
        this.card.className = 'card mb-3';

        // Create Header
        this.header = new hearderCard();
        this.headerTitle = new headerTitle(title);
        this.header.addElement(this.headerTitle.title);
        this.headerButton = new headerButton('#' + title.replace(/\s+/g, '') + 'Body');
        this.header.addElement(this.headerButton.button);

        // Create Body
        this.body = new cardBody(title.replace(/\s+/g, '') + 'Body');

        this.card.appendChild(this.header.heard);
        this.card.appendChild(this.body.collapse);

    }
    addGraph(dt, price,medianMove, tx){
        
        let div = document.createElement('div');
        let canvas = document.createElement('canvas');
        canvas.id = 'graphLine';

        this.graph = serieTitlePublic(canvas,dt, price,medianMove, tx);

        div.appendChild(canvas);

        this.body.addElement(div);
    }
    render(){

        let main = document.querySelector('main.container');

        main.appendChild(this.card);
        
    }    

}