FROM python:3.11

WORKDIR /helpandsupport

COPY . /helpandsupport

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /HELP/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]