FROM solr:9.3.0

USER root
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install pysolr
RUN pip3 install pandas
RUN pip3 install flask
RUN pip3 install flask_sqlalchemy
RUN pip3 install pandas as pd


WORKDIR /app

# Expose the Solr port
EXPOSE 8983
# Expose the Flask port
EXPOSE 8080

# run the webserver
CMD ["python3", "data.py"]