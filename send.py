import sys
import asyncio
import json
from time import time
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout


async def run(loop_obj):
    env = sys.argv[1]
    data_filename = sys.argv[2]
    configs = json.loads(open('configs.json', 'r').read())
    config = configs[env]
    
    nc = NATS()
    await nc.connect(servers=config['nats'])
    data = json.loads(open(data_filename, 'r').read())
    subject = data['subject']
    payload = json.dumps(data['payload']).encode()

    start = time()
    try:
        response = await nc.request(subject, payload, timeout=10)
        elapsed = time() - start
        print('--------------------')
        print(response.data.decode())
        print('--------------------')
        print('Timed:', elapsed)
        print('--------------------')
    except Exception as e:
        print('--------------------')
        print("Error:", e)
        print('--------------------')
    finally:
        await nc.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    loop.close()