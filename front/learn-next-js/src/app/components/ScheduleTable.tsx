import { promises as fs } from 'fs';
import {ScheduleInterface} from "@/interfaces/scheduleInterface"


async function CreateTable(schedule: ScheduleInterface) {
    const scheduleDaysAndShiftsTuples: [date: string, shifts: {[shift: string]: string; }[]][] = Object.entries(schedule)
    const firstDayInSchedule: [date: string, shifts: {[shift: string]: string; }[]] = scheduleDaysAndShiftsTuples[0]
    const scheduleDates: string[] = scheduleDaysAndShiftsTuples.map(([date]) => date)
  
    const tHeaders = scheduleDates.map((dateHeader) => <th className="p-1 text-black">{dateHeader}</th>)
    const dayInfoIndex = 1
    const shiftsTypes: string[] = Object.keys(firstDayInSchedule[dayInfoIndex])
  
	const tBody = shiftsTypes.map((shift) => 
	<tr className="divide-x-2 divide-slate-600">
		<th className="p-1 text-black">
			{shift}
		</th>
		{scheduleDaysAndShiftsTuples.map(([date, shifts]) => <td className="p-1 text-black">{shifts[shift]}</td>)}
	</tr>)


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