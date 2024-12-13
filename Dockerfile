FROM python:3.12
RUN mkdir /employee_schedule_project
WORKDIR /employee_schedule_project
RUN python -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./src ./src
COPY ./generate_openapi.py .
EXPOSE 8000
CMD python -m uvicorn --host 0.0.0.0 --port 8000 src.server.app:app