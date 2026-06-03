import { Link, useLocation } from 'react-router-dom'

const Navbar = () => {
    const location = useLocation()
    const isActive = (path) => location.pathname === path

    return (
        <nav className="navbar-glass fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-8 py-4">
            <Link to="/" className="text-xl font-bold gradient-text">
                Veritas
            </Link>

            <div className="flex gap-8">
                {[
                    { path: '/', label: 'Home' },
                    { path: '/evaluate', label: 'Evaluate' },
                    { path: '/results', label: 'Results' },
                ].map(({ path, label }) => (
                    <Link
                        key={path}
                        to={path}
                        className={`text-sm font-medium transition-all duration-300 ${
                            isActive(path)
                                ? 'text-green-400'
                                : 'text-gray-400 hover:text-white'
                        }`}
                    >
                        {label}
                    </Link>
                ))}
            </div>
        </nav>
    )
}

export default Navbar