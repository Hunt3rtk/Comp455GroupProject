FROM solr:9.4.0

COPY project.py /app/project.py

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install pysolr
RUN pip3 install pandas
RUN pip3 install tk

EXPOSE 8983

WORKDIR /app
# Open the project.py file
CMD ["python3", "project.py"]
