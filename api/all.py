import os
from threading import Thread

if __name__ == "__main__":
  Thread(target=lambda: os.system("python ./email/email.py")).start()
  Thread(target=lambda: os.system("python ./error/error.py")).start()
  Thread(target=lambda: os.system("python ./item/item.py")).start()
  Thread(target=lambda: os.system("python ./order/order.py")).start()
  Thread(target=lambda: os.system("python ./place_order/place_order.py")).start()
  Thread(target=lambda: os.system("python ./stripe_wrapper/stripe_wrapper.py")).start()
  Thread(target=lambda: os.system("python ./user/user.py")).start()
