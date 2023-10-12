from ortools.sat.python import cp_model


class ConstraintsModel:

    def __init__(self, week_info, employees):
        self.week_info = week_info
        self.employees = employees
        self.cp_model = cp_model.CpModel()
        self.all_possible_shifts_combo = {}
        self._populate_all_possible_shifts_combo()

    def _populate_all_possible_shifts_combo(self):

        for employee in self.employees:
            for day in range(len(self.week_info.days_in_this_week)):
                for shift in self.week_info.days_in_this_week[day].shifts:

                    day_name = self.week_info.days_in_this_week[day].today_is.value
                    # print(day_name, employee.name, shift.type)

                    self.all_possible_shifts_combo[(employee.name, day_name, shift.type)] = self.cp_model.NewBoolVar(
                        f"shift_employee{employee.name}_day{day_name}_shift{shift.type}"
                    )
