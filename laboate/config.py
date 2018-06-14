import ujson


def get_config():
    with open('config.json', 'r') as f:
        return ujson.load(f)
