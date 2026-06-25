import Card from '../Card'

function Section({title, description, items}) {
    return (
        <div>
            <div className="d-flex flex-column align-items-start gap-1 mt-4">
                <h2 className="text-center" id="section-title">{title}</h2>
                <p className="text-center" id="section-description">{description}</p>
            </div>
            <div className="d-flex justify-content-center align-items-center mt-5">
                {
                    items.map(card => {
                    
                        return <Card title={card.title} deadline={card.deadline} marketValue={card.marketValue} median={card.median} value={card.value} oportunity={card.oportunity} img={card.img.img}/>

                    })
                }
            </div>
        </div>

    )
}

export default Section