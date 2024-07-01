import numpy as np
# Enables the Digit Low Level API to be used in the action server
from digit_interface.low_level_api import DigitLLApi






def main():
    ip = "127.0.0.1"
    llapi = DigitLLApi(ip)
    obs = llapi.step()
    print(llapi.observation)


if __name__ == "__main__":
     main()


