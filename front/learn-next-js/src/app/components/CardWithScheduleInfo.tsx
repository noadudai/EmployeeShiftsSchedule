import CreateTable from "./ScheduleTable"


async function CardWithScheduleInfo(employees: object, scheduleData: object, schedule: object){
    const numberOfShiftsForEmployees = scheduleData.number_of_shifts
    const numberOfClosingShifts = scheduleData.number_closing_shifts
    const numberOfMorningShifts = scheduleData.number_morning_shifts
    
    const numShiftsEntries = Object.entries(numberOfShiftsForEmployees)
    const numClosingsEntries = Object.entries(numberOfClosingShifts)
    const numMorningsEntries = Object.entries(numberOfMorningShifts)

    const employeeIdIndex = 0
    const numShiftsIndex = 1
    const numberOfShifts = numShiftsEntries.map((entrie) => <p className="text-xs">{employees[entrie[employeeIdIndex]].employee_name} works {entrie[numShiftsIndex]} shifts.</p>)
    const numClosings = numClosingsEntries.map((entrie) => <p className="text-xs">{employees[entrie[employeeIdIndex]].employee_name} works {entrie[numShiftsIndex]} closing shifts.</p>)
    const numMornings = numMorningsEntries.map((entrie) => <p className="text-xs">{employees[entrie[employeeIdIndex]].employee_name} works {entrie[numShiftsIndex]} morning shifts.</p>)

    return (
        <div className="flex bg-white border shadow-sm rounded-xl">
          <div className="p-4 md:p-5 text-black">
            <h1 className="text-lg font-bold">Schedule Information</h1>
            <div className="space-y-4 p-4">
                <div>
                    <h3>Number of shifts for each employee:</h3>
                    {numberOfShifts}
                </div>
                <div>
                    <h3>Number of closing shifts for each employee:</h3>
                    {numClosings}
                </div>
                <div>
                    <h3>Number of morning shifts for each employee:</h3>
                    {numMornings}
                </div>
            </div>
            <div className='flex columns-2 justify-evenly '>
                <div className="relative group inline-block">
                    <button className="bg-slate-200 text-slate-500 px-3 py-2 rounded-lg hover:bg-slate-300 transition duration-300 ease-in-out transform">Peek</button>
                    <div className="opacity-0 invisible group-hover:opacity-100 group-hover:visible absolute bg-white text-gray-800 border border-gray-300 rounded-lg shadow-lg py-2">
                        {CreateTable(schedule)}
                    </div>
                </div>
                <button className="text-slate-500 font-bold px-3 py-2 bg-slate-200 rounded-lg hover:bg-slate-300">Select schedule</button>
            </div>
          </div>
        </div>
    );
}

export default CardWithScheduleInfo