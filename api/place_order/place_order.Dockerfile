FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./place_order.py ./invokes.py ./sns_controller.py ./stripe_controller.py  ./
CMD [ "python", "./place_order.py" ]