"use client"
import Link from 'next/link'

import createSchedules from "./CreateSchedules";
import { useState } from 'react';


const ScheduleOptionsNavbar = () => {

    // isModalVisible is connected to "Create schedule options", that will be implamented in a future feature.
    const [isModalVisible, setIsModalVisible] = useState(false);

    return (
        <div>
            <nav className="bg-white w-full rounded-lg shadow-sm">
                <div className="flex justify-between items-center py-8 px-4">
                    <div className="flex items-center pl-8">
                        <h1 className="text-4xl font-bold text-black">Schedule Options</h1>
                    </div>
                    <div className="flex space-x-3 pr-8">
                        <Link className="text-slate-500 font-bold px-3 py-2 bg-slate-200 rounded-lg hover:bg-slate-400 hover:underline hover:text-slate-700" href="/">Home Page</Link>
                        <div>  
                            <button data-modal-target="cretae-new-schedules" data-modal-toggle="cretae-new-schedules" className="text-slate-500 font-bold px-3 py-2 bg-slate-200 rounded-lg hover:bg-slate-200 hover:underline hover:text-slate-700">Create Schedule</button>
                        </div>
                        <button className="text-slate-500 font-bold px-3 py-2 bg-slate-200 rounded-lg hover:bg-slate-400 hover:underline hover:text-slate-700">Employees</button>
                    </div>
                </div>
            </nav>
            {isModalVisible && (
                <div id="cretae-new-schedules" className=" w-full p-4 overflow-x-hidden overflow-y-auto">
                    <div className="justify-center w-full max-w-md max-h-full bg-white rounded-lg shadow p-4 rounded-lg">
                        <h3 className="text-6xl font-medium text-slate-500">Creating new schedule options...</h3>
                    </div>
                </div>
            )}
        </div>
        
    );
}

export default ScheduleOptionsNavbar