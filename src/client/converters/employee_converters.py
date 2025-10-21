from src.client.api_models.employee_api_model import EmployeeApiModel
from src.client.api_models.employee_position_api_enum import EmployeePositionApiEnum
from src.client.api_models.employee_priority_api_enum import EmployeePriorityApiEnum
from src.client.api_models.employee_status_api_enmu import EmployeeStatusApiEnum
from src.client.api_models.shift_types_api_enum import ShiftTypesApiEnum
from src.models.employees.employee import Employee
from src.models.employees.employee_position_enum import EmployeePositionEnum
from src.models.employees.employee_priority_enum import EmployeePriorityEnum
from src.models.employees.employee_status_enum import EmployeeStatusEnum
from src.models.shifts.shifts_types_enum import ShiftTypesEnum


def api_employee_to_internal_employee(api_employee_model: EmployeeApiModel) -> Employee:
    return Employee(name=api_employee_model.name,
                    priority=EmployeePriorityEnum[api_employee_model.priority.name],
                    employee_status=EmployeeStatusEnum[api_employee_model.employee_status.name],
                    employee_id=api_employee_model.employee_id,
                    position=EmployeePositionEnum[api_employee_model.position.name],
                    shifts_preferences=api_employee_model.shifts_preferences,
                    shift_types_trained_to_do=list(ShiftTypesEnum[api_employee_shift_preference.name] for api_employee_shift_preference in api_employee_model.shift_types_trained_to_do))


def internal_employee_to_api_employee(employee: Employee) -> EmployeeApiModel:
    return EmployeeApiModel(name=employee.name,
                            priority=EmployeePriorityApiEnum[employee.priority.name],
                            employee_status=EmployeeStatusApiEnum[employee.employee_status.name],
                            employee_id=employee.employee_id,
                            position=EmployeePositionApiEnum[employee.position.name],
                            shifts_preferences=employee.shifts_preferences,
                            shift_types_trained_to_do=list(ShiftTypesApiEnum[employee_shift_preference.name] for employee_shift_preference in employee.shift_types_trained_to_do))
