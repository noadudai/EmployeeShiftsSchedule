from ortools.sat.python import cp_model


class Constraints:

    def __init__(self, week_info, employees):
        self.week_info = week_info
        self.employees = employees
        self.cp_model = cp_model.CpModel()
        self.all_possible_shifts_combo = self._generate_all_possible_shifts_combo(self.employees, self.week_info, self.cp_model)

    @staticmethod
    def _generate_all_possible_shifts_combo(employees, week_info, model):
        all_possible_shifts_combo = {}
        for employee in employees:
            for day in range(len(week_info.days_in_this_week)):
                day_name = week_info.days_in_this_week[day].today_is.value

                for shift in week_info.days_in_this_week[day].shifts:

                    all_possible_shifts_combo[(employee.name, day_name, shift.type)] = model.NewBoolVar(
                        f"shift_employee{employee.name}_day{day_name}_shift{shift.type}"
                    )

        return all_possible_shifts_combo

    # A constraint that ensures that there will be only one employee in each shift per day
    def one_employee_in_each_shift_constraint(self):

        for day in range(len(self.week_info.week)):
            day_name = self.week_info.days_in_this_week[day].today_is.value

            for shift in self.week_info.week[day].shifts:
                self.cp_model.AddExactlyOne(self.all_possible_shifts_combo[(employee.name, day_name, shift.shift_type)] for employee in self.employees)

    # A constraint that ensures that each employee works at most one shift per day
    def at_most_one_shift_a_day_constraint(self):
        for employee in self.employees:
            for day in range(len(self.week_info.week)):
                day_name = self.week_info.days_in_this_week[day].today_is.value

                self.cp_model.AddAtMostOne(self.all_possible_shifts_combo[(employee.name, day_name, shift.shift_type)] for shift in self.week_info.week[day].shifts)
