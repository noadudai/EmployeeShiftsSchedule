from setuptools import setup

setup(name='employee shift schedule',
      version='0.0.1',
      description='Package for creating an employee working schedule',
      author='Noa Dudai',
      author_email='dudai.noa@gmail.com',
      url='https://github.com/noadudai/EmployeeShiftsSchedule',
      install_requires=[
            'ortools',
            'pandas==2.0.3'
      ],
      packages=["employee_shift_schedule"]
      )
