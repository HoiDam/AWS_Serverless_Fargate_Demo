FROM python:3.7
WORKDIR /FargateTest
ADD . /FargateTest
RUN pip install -r requirements.txt
# EXPOSE 443
ENV NAME World
CMD ["python","trigger.py"]