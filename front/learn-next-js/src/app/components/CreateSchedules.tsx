async function createSchedules() {
    const response = await fetch(`${process.env.URL}/create-and-get-schedule-options`);
    if (!response.ok) {
        console.error('Failed to create data');
        const errorMessage = `An error hase occured: ${response.status}`;
        throw new Error(errorMessage);
    } else {
        console.log('schedules created!')
    }
}

export default createSchedules