const params = new URLSearchParams(window.location.search);

const tt = params.get("title");
const deadline = params.get("deadline");

let pathname = `/rendafixa/${tt}/${deadline}`

async function getDatas(){
    
    let request = new Request(pathname)
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

let data =  getDatas();
let ctx
let dt = [];
let tx = [];
let price = [];
let medianMove

data.then(
    (json) => {
        console.log(json)

        json.sort((a,b) => new Date(a['data']) - new Date(b['data']))
        console.log(json)
    
        
        json.map( (key) => {       
                dt.push(key.data)
                tx.push(key.taxa_compra_manha*100)
                price.push(key.pu_compra_manha)
            } 
        )

        medianMove = rolling(price, 20);
        const container = document.querySelector("main > .card > .card-body")
        ctx = document.createElement("canvas");
        ctx.className = "p-4"
        ctx.id="graph"

        let titleGraph = `Título Público - ${json[0].tipo} - ${json[0].vencimento}`

        document.querySelector("main > .card > .card-header").innerHTML = titleGraph;

        container.appendChild(ctx)
        serieTitlePublic(ctx, dt, price, medianMove, tx);
    }
)
