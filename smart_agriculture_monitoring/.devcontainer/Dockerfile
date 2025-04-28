# Use a Python image from Docker Hub
FROM mcr.microsoft.com/vscode/devcontainers/python:3.9

# Install system dependencies if necessary (e.g., for data science tools)
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev

# Install additional Python packages or tools if necessary
RUN pip install --upgrade pip
RUN pip install numpy pandas scikit-learn statsmodels tensorflow streamlit matplotlib seaborn pydeck kagglehub

# Set the working directory inside the container
WORKDIR /workspace

# Expose the port that Streamlit uses
EXPOSE 8501
