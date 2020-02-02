FROM python:3.5
RUN pip install flask
RUN pip install flask-restful
RUN pip install requests

RUN pip install pymongo
RUN pip install jupyterlab

RUN wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-278.0.0-linux-x86_64.tar.gz
RUN tar xvzf google-cloud-sdk-278.0.0-linux-x86_64.tar.gz -C google_cloud
RUN rm google-cloud-sdk-278.0.0-linux-x86_64.tar.gz


WORKDIR ./

