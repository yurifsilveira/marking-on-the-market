import NavBar from './NavBar'
import logo from  '../../assets/factorinvest.png'
import UserButton from './UseButton'


function Header(){

    const links = [
        { label: "Home", href: "#", active: true },
        { label: "Renda Fixa", href: "#" },
        { label: "Ações", href: "#" }
    ]

    const user = {
        name: "Yuri",
        image: null // ou URL do OAuth2 (ex: Google)
    }

    return(
        <header className="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3">
            <div className="col-md-3 mb-md-0"> 
                <a href="/" className="d-flex align-items-center justify-content-center text-decoration-none w-100">
                    <img src={logo} alt="icone-investimento" height="69" />
                    <h3 id="titulo-pagina" className="mb-0 p-0 m-1">FactorInvest</h3>
                </a>
            </div> 
            <NavBar links={links} />
            <UserButton 
                userName={user.name}
                userImage={user.image}
                onClick={() => console.log("Abrir menu do usuário")}
            />
        </header> 
    )
}

export default Header