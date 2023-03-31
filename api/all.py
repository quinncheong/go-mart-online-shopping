import os
from threading import Thread

def run(x):
  os.system(f"python ./{x}/{name}.py")

if __name__ == "__main__":
  Thread(target=lambda: os.system(f"python ./email/email.py")).start()
  Thread(target=lambda: os.system(f"python ./error/error.py")).start()
  Thread(target=lambda: os.system(f"python ./item/item.py")).start()
  Thread(target=lambda: os.system(f"python ./order/order.py")).start()
  Thread(target=lambda: os.system(f"python ./place_order/place_order.py")).start()
  Thread(target=lambda: os.system(f"python ./stripe_wrapper/stripe_wrapper.py")).start()
  Thread(target=lambda: os.system(f"python ./user/user.py")).start()
