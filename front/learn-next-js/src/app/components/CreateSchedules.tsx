async function createSchedules() {
    const response = await fetch(`${process.env.URL}/create-and_get_schedule-options`);
    if (!response.ok) {
        console.error('Failed to create data');
    } else {
        console.log('schedules created!')
    }
}

export default createSchedules