import Link from 'next/link'

const SideBar = ({isOpen, onClickHandler}: {isOpen: boolean, onClickHandler: ()=> void}) => {
    return (
        <div className={`mt-4 rounded-lg w-64 bg-white text-black transform ${isOpen? 'translate-x-100' : '-translate-x-full'} transition-transforme`}>
            <button onClick={onClickHandler} className='absolute top-4 right-4 text-2xl'>
                &times;
            </button>
            <nav className='flex flex-col space-x-4 space-y-4 p-4'>
                <div className="text-slate-500 font-bold px-3 py-2 ml-4 rounded-lg hover:bg-slate-200 hover:underline hover:text-slate-700">
                     <Link href="/">Home Page</Link>
                 </div>
                 <div className="text-slate-500 font-bold px-3 py-2 rounded-lg hover:bg-slate-200 hover:underline hover:text-slate-700" >
                     <Link href="/schedule-options">Schedule Options</Link>
                 </div>
                 <div>
                     <button className="text-slate-500 font-bold px-3 py-2 rounded-lg hover:bg-slate-200 hover:underline hover:text-slate-700">Employees</button>
                 </div>
            </nav>
        </div>
    );
  };

export default SideBar  