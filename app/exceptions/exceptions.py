class DepartmentNotFoundError(Exception):
    """Департамент не найден"""
    def __init__(self, department_id: int):
        self.department_id = department_id
        self.message = f"Department with id {department_id} not found"
        super().__init__(self.message)


class EmployeeNotFoundError(Exception):
    """Сотрудник не найден"""
    def __init__(self, employee_id: int):
        self.employee_id = employee_id
        self.message = f"Employee with id {employee_id} not found"
        super().__init__(self.message)
