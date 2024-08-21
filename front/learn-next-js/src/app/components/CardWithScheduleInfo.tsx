import CreateTable from "./ScheduleTable"


async function CardWithScheduleInfo(employees: object, scheduleData: object, schedule: {[date: string]: {[shift: string]: string}}){
    const numberOfShiftsForEmployees: {string : number} = scheduleData.number_of_shifts
    const numberOfClosingShifts: {string : number} = scheduleData.number_closing_shifts
    const numberOfMorningShifts: {string : number} = scheduleData.number_morning_shifts
    
    const numShiftsEntries: [employeeId: string, numberOfShifts: number][] = Object.entries(numberOfShiftsForEmployees)
    const numClosingsEntries: [employeeId: string, numberOfShifts: number][] = Object.entries(numberOfClosingShifts)
    const numMorningsEntries: [employeeId: string, numberOfShifts: number][] = Object.entries(numberOfMorningShifts)

    const numberOfShiftsJSX = numShiftsEntries.map(([employeeId, numShifts]) => <p className="text-xs">{employees[employeeId].employee_name} works {numShifts} shifts.</p>)
    const numClosingShiftsJSX = numClosingsEntries.map(([employeeId, numShifts]) => <p className="text-xs">{employees[employeeId].employee_name} works {numShifts} closing shifts.</p>)
    const numMorningShiftsJSX = numMorningsEntries.map(([employeeId, numShifts]) => <p className="text-xs">{employees[employeeId].employee_name} works {numShifts} morning shifts.</p>)

    return (
        <div className="flex bg-white border shadow-sm rounded-xl">
          <div className="p-4 md:p-5 text-black">
            <h1 className="text-lg font-bold">Schedule Information</h1>
            <div className="space-y-4 p-4">
                <div>
                    <h3>Number of shifts for each employee:</h3>
                    {numberOfShiftsJSX}
                </div>
                <div>
                    <h3>Number of closing shifts for each employee:</h3>
                    {numClosingShiftsJSX}
                </div>
                <div>
                    <h3>Number of morning shifts for each employee:</h3>
                    {numMorningShiftsJSX}
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