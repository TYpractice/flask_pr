FROM python:3.9

WORKDIR /app


COPY requirements.txt /app/requirements.txt
RUN echo "Installing packages..." && pip install --no-cache-dir -r requirements.txt && echo "Packages installed successfully"

COPY . /app

CMD ["flask", "run", "--host=0.0.0.0"]