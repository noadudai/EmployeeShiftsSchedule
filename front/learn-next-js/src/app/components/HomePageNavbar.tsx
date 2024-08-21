import React from 'react';

const HomePageNavbar = ({onClickSideBarHandler}: {onClickSideBarHandler: ()=> void}) => {
    return (
        <div className="bg-white w-full rounded-lg shadow-xl flex items-center py-8 px-4">
            <button onClick={onClickSideBarHandler} className="flex flex-col items-center justify-center w-7 h-7 rounded">
                <div className="block w-6 h-0.5 bg-slate-500 mb-1"></div>
                <div className="block w-6 h-0.5 bg-slate-500 mb-1"></div>
                <div className="block w-6 h-0.5 bg-slate-500"></div>
            </button>
            <div>
                <h1 className="text-6xl font-bold text-black ml-6">Home Page</h1>
            </div>
        </div>
    );
}

export default HomePageNavbar

