# 1. Use an official Python runtime as a parent image
FROM python:3.13

# 2. Set the working directory in the container
WORKDIR /usr/local/app

# 3. Copy the dependencies file to the working directory
COPY requirements.txt ./

# 4. Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application's source code
COPY src ./src

# 6. Make port 8080 available to the world outside this container
EXPOSE 8080

# 7. Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
