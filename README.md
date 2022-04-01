# NATS Person

## Configuration File

Configuration file name must be `config.json`

```json
{
    "local": {
        "nats": ["nats://localhost:4222"]
    },
    "remote": {
        "nats": ["nats://remote.com:4222]
    }
}
```

## Payload File

Here a sample of payload file

```json
{
    "subject": "nats.subject.sample",
    "payload": {
        "hello": "world"
    }
}
```

## Run

Here a sample how to run

```shell script
python send.py --env local --file sample.json --request-num 100
```

With this command, it will send *100* messages concurrently to NATS using
*sample.json* as payload and using *local* configuration.
