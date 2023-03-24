FROM python:3.9-slim
WORKDIR /user/arc/app
COPY ./requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./stripe_wrapper.py ./
CMD [ "python", "./stripe_wrapper.py" ]