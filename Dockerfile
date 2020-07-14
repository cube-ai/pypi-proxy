FROM unicom.gq:8801/python35-slim:0.0.1
WORKDIR /app
ADD . /app
RUN cd /app && mkdir packages
VOLUME "/app/packages"
RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple/
CMD python3 ./start.py
