import asyncio, time, random, os

from prometheus_client import start_http_server, Summary
from kasa import Discover, Module

from prometheus_client import Gauge

env_var = os.environ

if os.environ.get('INTERVAL') == None:
    INTERVAL = 5
else:
    INTERVAL = env_var['INTERVAL']

s = Gauge(env_var['GAUGE_NAME'], env_var['GAUGE_DESC'])
s.set(0)    # Initial set

async def main():
    try:
      dev = await Discover.discover_single(env_var['IP_ADDRESS'], username=env_var['USERNAME'], password=env_var['PASSWORD'])
      while True:
          await dev.update()
          energy = dev.modules["Energy"]
          s.set(energy.current_consumption)
          time.sleep(INTERVAL)
    except KeyError:
        print("Error. Please supply required parameters.")
        return

if __name__ == "__main__":
    start_http_server(10240)
    asyncio.run(main())