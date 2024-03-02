# Define the python version to use
FROM python:3.12.2

#Set the working directory to /src
WORKDIR /comando-api

# Copy the src folder that contains the scripts needed
COPY . /comando-api

# Install the requirements.txt file with all the libraries
RUN pip install -r requirements.txt


EXPOSE 8000

CMD ["uvicorn", "api:app","--reload", "--host", "0.0.0.0", "--port", "8000"]
