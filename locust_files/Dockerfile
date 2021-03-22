FROM python:3.9.1
# Add the licenses for third party software and libraries
ADD /docker-image/licenses /licenses
# Add the external tasks directory into /tasks
ADD /docker-image/locust-tasks /locust-tasks
RUN ls
COPY create_device_group.py .
# Install the required dependencies via pip
RUN pip install -r /locust-tasks/requirements.txt
# Expose the required Locust ports
EXPOSE 5557 5558 8089
# Set script to be executable
RUN chmod 755 /locust-tasks/run.sh
# Start Locust using LOCUS_OPTS environment variable

ENTRYPOINT ["/locust-tasks/run.sh"]
# ENTRYPOINT ["ls"]









