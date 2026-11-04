FROM python:3.13

ARG world
ARG AP_VERSION=main

RUN git clone -b $AP_VERSION --depth 1 https://github.com/ArchipelagoMW/Archipelago.git /Archipelago
WORKDIR /Archipelago

RUN python -m pip install -r requirements.txt
RUN python ./ModuleUpdate.py -a ./WebHostLib/requirements.txt -y

ADD scripts /scripts

RUN python -m pip install -r /scripts/requirements.txt


ENTRYPOINT ["/usr/local/bin/python3"]
CMD ["/scripts/run.py"]
