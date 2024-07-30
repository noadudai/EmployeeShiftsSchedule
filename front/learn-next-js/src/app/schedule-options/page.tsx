import ScheduleOptionsNavbar from '../components/ScheduleOptionsNavbar';
import CardWithScheduleInfo from '../components/CardWithScheduleInfo';

async function ScheduleOptions() {

  
    console.log("getting schedules")
    const response = await fetch("http://localhost:8000/get-schedules-solutions", {cache: "no-cache"});
    if (!response.ok) {
      return (
        <div className='p-4'>
          <ScheduleOptionsNavbar/>
          <div className='flex justify-center p-8'>
            <p className='text-9xl'>No schedules yet</p>
          </div>
        </div>
      )  
      // throw new Error('Failed to fetch data')
        
    } else {
        const data = await response.json();
        const schedules_info = data.schedules_info;
        const additionalData = data.additional_data;
        const additional_data_entries = Object.entries(additionalData)

        const employees = data.schedules_info.employees; 
        const scheduleDataIndex = 1

        const cardsSchedulesInfo = additional_data_entries.map((entrie) => <div>{CardWithScheduleInfo(employees, entrie[scheduleDataIndex], schedules_info.schedules[entrie[0]])}</div>)
      
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