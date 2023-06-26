FROM ubuntu:20.04
RUN apt update -y && apt-get install python3.8 python3.8-dev python3.8-distutils python3.8-venv -y
RUN apt install python3-pip -y 
RUN apt install git -y
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install software-properties-common -y && add-apt-repository ppa:swi-prolog/stable -y 
RUN apt-get update && apt-get install swi-prolog -y
WORKDIR /app
COPY src src
COPY requirements.txt requirements.txt
COPY setup.py setup.py
RUN pip3 install -r requirements.txt
COPY knowledge_base.pl knowledge_base.pl
ENTRYPOINT [ "python3", "-m", "flask", "--app", "src/app.py", "run", "--host", "0.0.0.0"]