let deadline = "2050-08-15"
let url_title = `http://localhost:8000/investimento/renda_fixa/titulopublico?limit=10000000000&tipo=NTN&deadline${deadline}`

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

let data =  getDatas();
let ctx
let dt = [];
let tx = [];
let price = [];
let medianMove
data.then((json) =>{

 
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
 


    json.map( (key) => {       
            dt.push(key.data)
            tx.push(key.taxa_compra_manha*100)
            price.push(key.pu_compra_manha)
        } 
    )

    medianMove = rolling(price, 20);
    const container = document.querySelector("main")
    ctx = document.createElement("canva");
    ctx.id="graph"

    container.appendChild(ctx)


})

requestAnimationFrame(() => {
    serieTitlePublic(ctx, dt, price, medianMove, tx);
});