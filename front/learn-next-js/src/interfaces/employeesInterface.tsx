export  interface EmployeesInterface {
    name: string;
    priority: string;
    employee_status: string;
    employee_id: string;
    position: string;
    // preferences is an object containing the employees preferred schedule.
    preferences: unknown;
    shift_types_trained_to_do: string[];
}