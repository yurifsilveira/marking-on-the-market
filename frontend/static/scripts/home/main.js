let url_title = "http://127.0.0.1:5000/cards"

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
let json

getDatas().then( (json) => {

    let summ = document.getElementById("summaries");
    json.titulos_publicos.sort((a,b) => b.vencimento - a.vencimento)

    let types = [...new Set(json.titulos_publicos.map(t => t.tipo))];

    for (let type of types)
    {    
        let div = new Card(json.titulos_publicos.sort((a, b) => new Date(b.vencimento) - new Date(a.vencimento)).filter(row => row.tipo == type), "Títulos Públicos - " + type).render()
        summ.appendChild(div)
    }
})
