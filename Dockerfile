From ubuntu:18.04

RUN apt-get update -y
RUN apt-get install -y apt-utils
RUN apt-get install -y build-essential libssl-dev libffi-dev python-dev python3-venv
RUN apt-get install -y git python3-pip
RUN pip3 install wheel setuptools
RUN apt-get install -y ffmpeg

RUN cd home && git clone https://github.com/Lin2D2/Discord_Music_Bot.git
RUN cd home/Discord_Music_Bot && python3 -m venv venv

RUN cd home/Discord_Music_Bot && . venv/bin/activate && pip3 install git+https://github.com/Rapptz/discord.py.git
RUN cd home/Discord_Music_Bot && . venv/bin/activate && pip3 install -r requirements.txt && pip3 install -U discord.py[voice]
