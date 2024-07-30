import { promises as fs } from 'fs';


async function CreateTable(schedule: []) {
    const scheduleEnries = Object.entries(schedule)
    const firstSchedule = scheduleEnries[0]
    const scheduleDates = scheduleEnries.map((entrie) => entrie[0])
  
    const tHeaders = scheduleDates.map((header) => <th className="p-1 text-black">{header}</th>)
  
    const shiftsTypes = Object.keys(firstSchedule[1])
  
    const rowHeaders = shiftsTypes.map((header) => <th className="p-1 text-black">{header}</th>)
  
    const tBody = new Array
  
    for(var i = 0; i < shiftsTypes.length; i++) {
      tBody.push(
        <tr className="divide-x-2 divide-slate-600">
          {rowHeaders[i]}
          {/* day[1][shiftTypes[i]] represents the information on thet "cell" in the schedule*/}
          {scheduleEnries.map((day) => <td className="p-1 text-black">{day[1][shiftsTypes[i]]}</td>)}
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