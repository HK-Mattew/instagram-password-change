FROM python:3
RUN pip3 install requests
COPY ./* ./
CMD [ "python3", "instagram_pwd_change.py" ]