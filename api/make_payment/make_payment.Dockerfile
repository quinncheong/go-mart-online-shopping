FROM python:3-slim
WORKDIR /user/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./make_payment.py ./invokes.py ./
CMD ["python", "./make_payment.py"]