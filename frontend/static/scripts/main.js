let url_title = "http://localhost:8000/investimento/renda_fixa/titulopublico?limit=10000000000&tipo=NTN"

async function getDatas(){
    
    let request = new Request(url_title)
    try {

    const response = await fetch(request);

    if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
    }

    const result = await response.json();

    return result

    } catch (error) {
    console.error(error.message);
    }    

}

let data = getDatas();

data.then( (json) => {

    let type = json[0].tipo;
    
    json.sort(
        (a,b) => {
            if (a.data > b.data){
                return 1
            }
            else {
                return -1
            }
        }
    )

    let deadlines = [...new Map(json.map(item => [item.vencimento, item.vencimento])).values()];

    deadlines.sort(
            (a,b) => { 
            if (a > b){
                return 1
            }
            return -1
        }
    )
    
    for (deadline of deadlines){

        let dt = [];
        let tx = [];
        let price = [];
        

        json.filter(item => item.tipo == type && item.vencimento == deadline).map( (key) => {       
                
                dt.push(key.data)
                tx.push(key.taxa_compra_manha*100)
                price.push(key.pu_compra_manha)
            } 
        )
        let medianMove = rolling(price, 20);
        let titlePublic = new card(type + " " + deadline);
        titlePublic.addGraph(dt, price, medianMove, tx);
        titlePublic.render();

    }

})
