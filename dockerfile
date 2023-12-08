FROM solr:9.4.0

USER root
RUN apt-get update && apt-get install -y python3 python3-pip

COPY project.py /app/project.py

WORKDIR /app

# Expose the Solr port
EXPOSE 8983

# Run the project file
CMD ["python3", "project.py"]