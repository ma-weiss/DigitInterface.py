import asyncio

# Enables the Agiligy JSON API to be used in the action server
import agility as agility
import agility.messages as msgs

# Enables the Digit Low Level API to be used in the action server
from digit_interface.low_level_api import DigitLLApi


async def run_sim(api):#

        # sim_reset = msgs.SimulatorReset()
        # await api.send(sim_reset)

        sim_pause = msgs.SimulatorPause()
        await api.send(sim_pause)

        llapi = DigitLLApi()

        print(llapi.observation)
        print(llapi.command)

        # run step to get observation
        obs = llapi.step() # can also pass in a command here 
        # obs = llapi.step(torque_command=torque_command,  # default is zeros
        #                  velocity_command=velocity_command, # default is zeros
        #                  damping_command=damping_command, # default is zeros
        #                  apply_command=apply_command)  # default is False
        sim_step = msgs.SimulatorStep(dt=0.005)
        while obs['time'] < 60:
            await api.send(sim_step)
            await api.send(sim_pause)
            obs = llapi.step()  
            # print obs time 
            print('time: ', obs['time'], end='\r')

        await api.close()



def start(api, loop):
    """
    Starts the action server
    and keeps it alive.
    """
    loop.run_until_complete(start_api(api, loop))

async def start_api(api, loop):
    """
    Connects to the digit and
    keeps the connection alive.
    """
    await api.connect()
    await api.request_privilege("change-action-command")
    print('Connected to the Digit')
    asyncio.ensure_future(run_sim(api))
    

    while True:
        await asyncio.sleep(0.5)  # this keeps the connection alive
    return




def main():
    ip = "127.0.0.1"

    loop = asyncio.get_event_loop()
    api = agility.JsonApi()
    start(api, loop)

if __name__ == "__main__":
    main()



