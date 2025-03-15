# Stage 1: Builder - Install dependencies in a temporary layer
FROM python:3.12 AS builder

# Set the working directory
WORKDIR /app

# Copy only the requirements file to leverage Docker cache for dependencies
COPY requirements.txt /app

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Stage 2: Final Stage - Copy necessary files and set up the environment
FROM python:3.12 AS final

# Set the working directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/downloads /app/data /app/logs

# Copy only necessary files from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the project files into the final image
COPY . /app

# Make all scripts executable
RUN chmod +x /app/*.sh

# Debug to check that files are in the right directories
RUN ls /app && ls /app/data

# Set environment variables for flexibility
ARG ENV=development
ENV ENV=${ENV}

# Optional debug line to confirm environment variable setup
RUN echo "Environment set to $ENV"

# Define the entry point to run the renamed scripts sequentially
ENTRYPOINT ["/bin/bash", "-c", "\
echo 'Running data preparation...' ; \
/app/100_1_run_extract_debit_txns.sh ; \
exit_code=$? ; echo 'Return code for data preparation: '$exit_code ; \
\
echo 'Running data ingestion...' ; \
/app/100_2_run_data_ingestion_debit.sh ; \
exit_code=$? ; echo 'Return code for data ingestion: '$exit_code "]

