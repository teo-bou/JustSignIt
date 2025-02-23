import React from 'react';

const Header = () => {
    return (
        <header className="bg-white p-4 flex items-center shadow-md">
            <div className="flex-shrink-0">
                <h1 className="text-2xl font-impact text-black">Just Sign It</h1>
            </div>
            <nav className="ml-auto">
                <ul className="flex space-x-4">
                    <li>
                        <a href="/" className="text-black hover:text-gray-600 transition duration-300 ease-in-out">Home</a>
                    </li>
                    <li>
                        <a href="/practice" className="text-black hover:text-gray-600 transition duration-300 ease-in-out">Practice</a>
                    </li>
                    <li>
                        <a href="/leaderboard" className="text-black hover:text-gray-600 transition duration-300 ease-in-out">Leaderboard</a>
                    </li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;
