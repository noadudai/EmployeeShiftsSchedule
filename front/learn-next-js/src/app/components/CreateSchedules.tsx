async function createSchedules() {
    const response = await fetch("http://localhost:8000/create-schedules");
    if (!response.ok) {
        console.error('Failed to create data');
    } else {
        console.log('schedules created!')
    }
}

export default createSchedules