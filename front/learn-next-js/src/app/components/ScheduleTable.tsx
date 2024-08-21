import { promises as fs } from 'fs';


async function CreateTable(schedule: {[date: string]: {[shift: string]: string}}) {
    const scheduleDaysAndShiftsTuples: [date: string, shifts: {[shift: string]: string; }][] = Object.entries(schedule)
    const firstDayInSchedule: [date: string, shifts: {[shift: string]: string; }] = scheduleDaysAndShiftsTuples[0]
    const scheduleDates: string[] = scheduleDaysAndShiftsTuples.map(([date]) => date)
  
    const tHeaders = scheduleDates.map((dateHeader) => <th className="p-1 text-black">{dateHeader}</th>)
    const dayInfoIndex = 1
    const shiftsTypes: string[] = Object.keys(firstDayInSchedule[dayInfoIndex])
  
    const rowHeaders = shiftsTypes.map((header) => <th className="p-1 text-black">{header}</th>)
  
    const tBody = new Array
  
    for(var i = 0; i < shiftsTypes.length; i++) {
      tBody.push(
        <tr className="divide-x-2 divide-slate-600">
          {rowHeaders[i]}
          {/* represents the information on thet "cell" in the schedule*/}
          {scheduleDaysAndShiftsTuples.map(([date, shifts]) => <td className="p-1 text-black">{shifts[shiftsTypes[i]]}</td>)}
        </tr>
      )
    }
    
    return (
      <div className="flex shadow-md justify-center border-slate-600 border-2 rounded-lg">
        <table className="table-auto min-w-min min-h-min divide-y-2 divide-x-2 divide-slate-600 table-auto border-collapse content-evenly bg-white">
          <thead>
            <tr className="divide-x-2 divide-slate-600">
              {/* Empty table header for the shift types row */}
              <th></th>
              {tHeaders}
            </tr>
          </thead>
          <tbody className="divide-y-2 divide-slate-600">
            {tBody}
          </tbody>
        </table>
      </div>
    );
}

export default CreateTable 