import uuid
from collections import defaultdict
from typing import List

from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import IntVar

from src.models.employees.employee import Employee
from src.models.shifts.shift import Shift
from src.models.shifts.shift_combinations_key import ShiftCombinationsKey
from src.models.shifts.shifts_types_enum import ShiftTypesEnum
from src.models.solution.number_of_shifts_assigned_to_employee import NumberOfShiftsAssignedToEmployee
from src.models.solution.one_schedule_solution_metadata import ScheduleSolutionMetadata
from src.models.solution.schedule_shift_assignment import ScheduleShiftAssignment


class ScheduleSolutions:

    def __init__(self, solver: cp_model.CpSolver, all_shifts: dict[ShiftCombinationsKey, IntVar], employees: list[Employee], shifts: list[Shift], constraint_model: cp_model.CpModel):
        self.solver = solver
        self.all_shifts = all_shifts
        self.employees = employees
        self.shifts = shifts
        self.constraint_model = constraint_model

    def yield_schedules(self):
        while True:
            status = self.solver.Solve(self.constraint_model)
            if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:

                num_closings_for_employees: defaultdict[uuid.UUID, int] = defaultdict(int)
                num_mornings_for_employees: defaultdict[uuid.UUID, int] = defaultdict(int)
                num_shift_for_employees: defaultdict[uuid.UUID, int] = defaultdict(int)

                schedule: dict[uuid.uuid4(), uuid.uuid4()] = {}

                for employee in self.employees:
                    for shift in self.shifts:
                        if self.solver.Value(self.all_shifts[ShiftCombinationsKey(employee.employee_id, shift.shift_id)]):
                            schedule[shift.shift_id] = employee.employee_id

                            num_shift_for_employees[employee.employee_id] += 1

                            if shift.shift_type == ShiftTypesEnum.CLOSING:
                                num_closings_for_employees[employee.employee_id] += 1

                            if shift.shift_type in [ShiftTypesEnum.MORNING, ShiftTypesEnum.MORNING_BACKUP,
                                                    ShiftTypesEnum.WEEKEND_MORNING,
                                                    ShiftTypesEnum.WEEKEND_MORNING_BACKUP]:
                                num_mornings_for_employees[employee.employee_id] += 1

                closing_shifts_assignments: List[NumberOfShiftsAssignedToEmployee] = [NumberOfShiftsAssignedToEmployee(employee_id=str(key), number_of_shifts=val) for (key, val) in num_closings_for_employees.items()]
                morning_shifts_assignments: List[NumberOfShiftsAssignedToEmployee] = [NumberOfShiftsAssignedToEmployee(employee_id=str(key), number_of_shifts=val) for (key, val) in num_mornings_for_employees.items()]
                shifts_assignments: List[NumberOfShiftsAssignedToEmployee] = [NumberOfShiftsAssignedToEmployee(employee_id=str(key), number_of_shifts=val) for (key, val) in num_shift_for_employees.items()]

                schedule_shifts_assignments: List[ScheduleShiftAssignment] = [ScheduleShiftAssignment(shift_id=key, employee_id=val) for key, val in schedule.items()]

                solution = ScheduleSolutionMetadata(closing_shifts_assignments, morning_shifts_assignments,
                                                    shifts_assignments, schedule_shifts_assignments)

                # After a schedule was created, forbid the model to assign one of the assignments again
                # (make a new schedule entirely)
                all_schedule_assignments = [self.all_shifts[ShiftCombinationsKey(assignment.employee_id, assignment.shift_id)] for
                                            assignment in solution.schedule]
                all_schedule_un_assignments = []

                for assignment in all_schedule_assignments:
                    all_schedule_un_assignments.append(self.constraint_model.NewBoolVar(f"unassign_{assignment}"))

                for i in range(len(all_schedule_assignments)):
                    self.constraint_model.Add(
                        all_schedule_assignments[i] != self.solver.Value(all_schedule_assignments[i])).OnlyEnforceIf(
                        all_schedule_un_assignments[i])
                    self.constraint_model.Add(
                        all_schedule_assignments[i] == self.solver.Value(all_schedule_assignments[i])).OnlyEnforceIf(
                        all_schedule_un_assignments[i].Not())

                self.constraint_model.AddBoolOr(all_schedule_un_assignments)

                yield solution
