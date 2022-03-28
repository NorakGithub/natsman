import argparse
from ast import parse
import sys
import asyncio
import json
import time
from datetime import datetime
from nats.aio.client import Client as NATS

parser = argparse.ArgumentParser()
parser.add_argument('--env', '-e', action='store', type=str)
parser.add_argument('--file', '-f', action='store', type=str)
parser.add_argument('--request-num', '-n', action='store', type=int, default=1)


async def request(nc: NATS, subject, payload, timeout):
    start_datetime = datetime.now()
    start = time.perf_counter()
    response = await nc.request(subject, payload, timeout=timeout)
    total = time.perf_counter() - start
    finished_datetime = datetime.now()
    print(
        response.data.decode(),
        start_datetime,
        finished_datetime,
        'Req:', total
    )
    return response


async def run(env: str, filename: str, req_num: str):
    configs = json.loads(open('configs.json', 'r').read())
    config = configs[env]
    servers = config['nats']

    print('NATS servers:', servers)
    
    nc = NATS()
    await nc.connect(servers=servers)
    data = json.loads(open(filename, 'r').read())
    subject = data['subject']
    print('Subject:', subject)
    payload = json.dumps(data['payload']).encode()

    start = time.perf_counter()
    try:
        print('--------------------')
        requests = [
            request(nc, subject, payload, timeout=40)
            for _ in range(0, req_num)
        ]
        await asyncio.gather(*requests)
        elapsed = time.perf_counter() - start
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
    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(args.env, args.file, args.request_num))
    loop.close()
