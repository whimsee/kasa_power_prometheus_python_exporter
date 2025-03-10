import asyncio, time, os

from prometheus_client import start_http_server, Summary
from kasa import Discover, Module

from prometheus_client import Gauge

env_var = os.environ

if os.environ.get('INTERVAL') == None:
    INTERVAL = 5
else:
    INTERVAL = env_var['INTERVAL']

s1 = Gauge(env_var['GAUGE_NAME1'], env_var['GAUGE_DESC1'])
s2 = Gauge(env_var['GAUGE_NAME2'], env_var['GAUGE_DESC2'])

# Initial set
s1.set(0)
s2.set(0) 

async def main():
    try:
      dev1 = await Discover.discover_single(env_var['IP_ADDRESS1'], username=env_var['USERNAME'], password=env_var['PASSWORD'])
      dev2 = await Discover.discover_single(env_var['IP_ADDRESS2'], username=env_var['USERNAME'], password=env_var['PASSWORD'])
      while True:
          await dev1.update()
          await dev2.update()
          
          energy1 = dev1.modules["Energy"]
          energy2 = dev2.modules["Energy"]
          
          s1.set(energy1.current_consumption)
          s2.set(energy2.current_consumption)
          
          time.sleep(INTERVAL)
    except KeyError:
        print("Error. Please supply required parameters.")
        return

if __name__ == "__main__":
    start_http_server(10240)
    asyncio.run(main())
