import React from 'react';

const HomePageNavbar = ({onClickHandler}: {onClickHandler: ()=> void}) => {
    return (
        <div className="bg-white w-full rounded-lg shadow-xl flex items-center py-8 px-4">
            <button onClick={onClickHandler} className="flex flex-col items-center justify-center w-7 h-7 rounded">
                <span className="block w-6 h-0.5 bg-slate-500 mb-1"></span>
                <span className="block w-6 h-0.5 bg-slate-500 mb-1"></span>
                <span className="block w-6 h-0.5 bg-slate-500"></span>
            </button>
            <div>
                <h1 className="text-6xl font-bold text-black ml-6">Home Page</h1>
            </div>
        </div>
    );
}

export default HomePageNavbar

