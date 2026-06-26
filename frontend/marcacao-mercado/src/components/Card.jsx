import openLink from '../assets/open.png'

function Card({title, deadline, marketValue, median, value, oportunity, img}){
    
    const status = value > marketValue || value > median ? 'danger' : 'success';
    return <div className="card mb-4 w-100">
        <div className="card-bordy row">
            <div className="col-3 d-flex align-items-center">
                <div>
                    <img src={img} alt={title} className="icone"/>
                </div>
                <div className="d-flex flex-column justify-content-start align-items-start ms-2">
                    <h5 className="card-title title">{title}</h5>
                    <p className="card-text subtitle">Venc: {deadline}</p>
                </div>
            </div>
            <div className="col-3 d-flex flex-column justify-content-center align-items-center">
                <div className="d-flex flex-column justify-content-center align-items-start">
                    <p className="card-text">Preço Unitário: R$ {marketValue}</p>
                    <p className="card-text">Média Móvel: R$ {median}</p>
                </div>
            </div>
            <div className="col-3 d-flex flex-column justify-content-center align-items-center">
                <div className="d-flex flex-column justify-content-center align-items-start">
                    <p className={`card-text value text-${status}`}>Preço Carteira: R$ {value}</p>
                    <p className={`card-text value text-${status}`}>Marcação Mercado: R${Math.abs(oportunity)}</p>
                </div>
            </div>
            <div className="col-2 d-flex justify-content-center align-items-center">
                {oportunity > 0 ? <span className="btn-red d-flex justify-content-center align-items-center">Compra</span> : <span className="btn-green d-flex justify-content-center align-items-center">Venda</span>}
            </div>
            <div className="col-1 d-flex justify-content-center align-items-center">
                <button className='btn' onClick={() => window.open('http://localhost:5173/', '_blank', 'width=600,height=400')}>
                    <img src={openLink} alt="links" />
                </button>
            </div>
        </div>
    </div>
}

export default Card;