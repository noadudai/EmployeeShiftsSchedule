from setuptools import setup

setup(name='employee shift schedule',
      version='0.0.1',
      description='Package for creating an employee working schedule',
      author='Noa Dudai',
      author_email='dudai.noa@gmail.com',
      url='https://github.com/noadudai/EmployeeShiftsSchedule',
      install_requires=[
          'ortools==9.7.2996',
          'more-itertools==10.1.0',
          'fastapi==0.111.0',
          'anyio==3.7.1',
          'h11==0.12.0',
          'pandas==2.0.3',
          'numpy==2.2.0'
      ],
      tests_require=['pytest'],
      )
