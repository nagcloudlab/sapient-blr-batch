

function Navbar({ title }) {
    return (
        <nav className="navbar bg-body-tertiary">
            <div className="container-fluid">
                <a className="navbar-brand" href="#">{title}</a>
            </div>
        </nav>
    );
}

export default Navbar;