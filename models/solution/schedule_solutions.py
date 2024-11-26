import uuid
from collections import defaultdict

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import IntVar

from models.employees.employee import Employee
from models.shifts.shift import Shift
from models.shifts.shift_combinations_key import ShiftCombinationsKey
from models.shifts.shifts_types_enum import ShiftTypesEnum
from models.solution.one_schedule_solution_metadata import ScheduleSolution


class ScheduleSolutions:

    def __init__(self, solver: cp_model.CpSolver):
        self.solver = solver

    def yield_schedules(self, num_solutions: int, all_shifts: dict[ShiftCombinationsKey, IntVar], employees: list[Employee], shifts: list[Shift], constraint_model: cp_model.CpModel):
        counter = 0

        while counter <= (num_solutions - 1):

            status = self.solver.Solve(constraint_model)

            if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
                counter += 1

                num_closings_for_employees: defaultdict[uuid.UUID, int] = defaultdict(int)
                num_mornings_for_employees: defaultdict[uuid.UUID, int] = defaultdict(int)
                num_shift_for_employees: defaultdict[uuid.UUID, int] = defaultdict(int)

                schedule: dict[uuid.uuid4(), uuid.uuid4()] = {}

                for employee in employees:
                    for shift in shifts:
                        if self.solver.Value(all_shifts[ShiftCombinationsKey(employee.employee_id, shift.shift_id)]):
                            schedule[shift.shift_id] = employee.employee_id

                            num_shift_for_employees[employee.employee_id] += 1

                            if shift.shift_type == ShiftTypesEnum.CLOSING:
                                num_closings_for_employees[employee.employee_id] += 1

                            if shift.shift_type in [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP,
                                                    ShiftTypesEnum.WEEKEND_MORNING,
                                                    ShiftTypesEnum.WEEKEND_MORNING_BACKUP]:
                                num_mornings_for_employees[employee.employee_id] += 1

                solution = ScheduleSolution(num_closings_for_employees, num_mornings_for_employees,
                                            num_shift_for_employees, schedule)

                yield solution

                # After a schedule was created, forbid the model to assign one of the assignments again
                # (make a new schedule entirely)
                all_schedule_assignments = [all_shifts[ShiftCombinationsKey(employee_id, shift_id)] for shift_id, employee_id in solution.schedule.items()]
                all_schedule_un_assignments = []

                for assignment in all_schedule_assignments:
                    all_schedule_un_assignments.append(constraint_model.NewBoolVar(f"unassign_{assignment}"))

                for i in range(len(all_schedule_assignments)):
                    constraint_model.Add(all_schedule_assignments[i] != self.solver.Value(all_schedule_assignments[i])).OnlyEnforceIf(all_schedule_un_assignments[i])
                    constraint_model.Add(all_schedule_assignments[i] == self.solver.Value(all_schedule_assignments[i])).OnlyEnforceIf(all_schedule_un_assignments[i].Not())

                constraint_model.AddBoolOr(all_schedule_un_assignments)
