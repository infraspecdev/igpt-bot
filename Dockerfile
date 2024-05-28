FROM python
WORKDIR /home/
COPY . /home/
RUN pip install -r requirements.txt
CMD python main.py
