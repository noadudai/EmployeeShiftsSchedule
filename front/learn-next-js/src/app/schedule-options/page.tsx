import ScheduleOptionsNavbar from '../components/ScheduleOptionsNavbar';
import CardWithScheduleInfo from '../components/CardWithScheduleInfo';
import { AdditionalDataInterface } from '@/interfaces/additionalDataInterface';

async function ScheduleOptions() {

  
    console.log("getting schedules")
    const response = await fetch(`${process.env.URL}/create-and-get-schedule-options`, {cache: "no-cache"});
    if (!response.ok) {
      return (
        <div className='p-4'>
          <ScheduleOptionsNavbar/>
          <div className='flex justify-center p-8'>
            <p className='text-9xl'>No schedules yet</p>
          </div>
        </div>
      )  
      
    } else {
        console.log("schedules received")
        const data = await response.json();
        const schedules_info = data.schedules_info;

        const additionalData = data.additional_data;
        const additional_data_entries = Object.entries(additionalData)

        const employees = data.schedules_info.employees; 
        
        const scheduleDataIndexInEntry = 1
        const scheduleIndexInEntry = 0

        const cardsSchedulesInfo = additional_data_entries.map((entrie) => <div>{CardWithScheduleInfo(employees, entrie[scheduleDataIndexInEntry], schedules_info.schedules[entrie[scheduleIndexInEntry]])}</div>)
      
        return (
          <div className="p-4 ">
            <ScheduleOptionsNavbar/>
            <div className="flex">
              <div className="grid grid-flow-dense grid-cols-5 gap-x-4 mt-4">
                {cardsSchedulesInfo}
              </div>
            </div>
          </div>
        );
      }
    
  }
  
  export default ScheduleOptions;