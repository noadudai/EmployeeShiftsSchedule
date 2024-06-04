from models.employees.employees_file import all_employees
from models.shifts.shifts_file import all_shifts_in_the_week
from static_site.create_schedule_tables import create_schedule_options, data_frame_schedule_to_html_table, \
    replace_html_tables_content_with_new_schedule_tables

if __name__ == "__main__":
    employees = all_employees
    shifts = all_shifts_in_the_week
    number_of_solutions = 3

    try:
        schedule = create_schedule_options(employees, shifts, number_of_solutions)
        all_schedules = ''
        for solution in range(len(schedule.solutions)):
            # starts from 0
            all_schedules += f'solution {solution + 1}\n' + data_frame_schedule_to_html_table(
                schedule.solutions[solution].schedule, shifts, employees) + '<br><br>'

            replace_html_tables_content_with_new_schedule_tables(all_schedules, "visual_schedule.html")
    except Exception as e:
        print(e)
