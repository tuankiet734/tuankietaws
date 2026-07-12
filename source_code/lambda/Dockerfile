FROM public.ecr.aws/lambda/python:3.11

# Install system dependencies
RUN yum update -y && yum install -y gcc gcc-c++ postgresql-devel

# Copy requirements.txt to Lambda task root
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Upgrade pip to support modern manylinux wheels
RUN pip install --upgrade pip

# Install required python packages
RUN pip install --no-cache-dir -r requirements.txt mangum boto3 joblib

# Copy application code to Lambda task root
COPY lambda_app.py ${LAMBDA_TASK_ROOT}

# Set the CMD to the handler function in lambda_app.py
CMD [ "lambda_app.handler" ]
