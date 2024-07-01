import numpy as np
# Enables the Digit Low Level API to be used in the action server
from digit_interface.low_level_api import DigitLLApi

from datetime import datetime
from time import sleep




def main():
    ip = "127.0.0.1"
    llapi = DigitLLApi(ip)
    obs = llapi.step()
    print(llapi.observation)


    loop_time = 0.01
    times = []
    loop_times = []
    last_loop_start = datetime.now()
    # while True :
    for i in range(100):
        last_loop_start = datetime.now()
        obs = llapi.step()
        print(obs['time'])
        times.append(obs['time'])
        _delta = (datetime.now() - last_loop_start) 
        time_diff = _delta.total_seconds()

        loop_times.append(time_diff)
        
        if time_diff < loop_time:
            sleep(loop_time - time_diff)

    print(np.diff(np.array(times)))
    print(np.mean(np.diff(np.array(times))))
    print(np.std(np.diff(np.array(times))))
        
    print(np.mean(loop_times))
    print(np.std(loop_times))
        


if __name__ == "__main__":
     main()


