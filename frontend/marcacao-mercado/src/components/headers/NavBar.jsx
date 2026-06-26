
export function NavBar({ links }) {
    return (
        <ul className="nav col-12 col-md-auto justify-content-center mb-md-0">
            {links.map((link, index) => (
                <li key={index}>
                    <a 
                        href={link.href} 
                        className={`nav-link px-2 ${link.active ? "link-secondary" : "text-black"}`}
                    >
                        {link.label}
                    </a>
                </li>
            ))}
        </ul>
    )
}

export default NavBar