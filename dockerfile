FROM solr:9.3.0

USER root
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install pysolr
RUN pip3 install pandas
RUN pip3 install tk


COPY project.py /app/project.py

WORKDIR /app

# Expose the Solr port
EXPOSE 8983

# Run the project file
CMD ["python3", "project.py"]