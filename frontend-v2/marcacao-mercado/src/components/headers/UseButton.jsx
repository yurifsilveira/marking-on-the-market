export function UserButton({ userImage, userName = "U", onClick }) {

    // fallback: pega primeira letra do nome
    const initial = userName.charAt(0).toUpperCase()

    return (
        <div className="col-md-3 d-flex justify-content-end">
            <button 
                className="btn d-flex align-items-center justify-content-between py-1 rounded-pill border-secondary"
                onClick={onClick}
                id = "btn-login"
            >
                {/* Ícone menu */}
                <span className="me-2 fs-5">&#9776;</span>

                {/* Avatar */}
                <span
                    className="rounded-circle d-flex align-items-center justify-content-center overflow-hidden"
                    style={{ width: "36px", height: "36px", fontSize: "12px", backgroundColor: "#dc3545", color: "white" }}
                >
                    {userImage ? (
                        <img 
                            src={userImage} 
                            alt="user" 
                            style={{ width: "100%", height: "100%", objectFit: "cover" }}
                        />
                    ) : (
                        initial
                    )}
                </span>
            </button>
        </div>
    )
}

export default UserButton