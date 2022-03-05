import json
import os


def combine(a, b):
    a.update(b)
    return a


CONFIG_PATH = f"{os.getenv('HOME')}/.rdev/configs.json"
sections = json.loads(open(CONFIG_PATH).read())["sections"]
k8s_data = json.loads(open(CONFIG_PATH).read())["k8s-configs"]
sections = [combine(item, {"id": f"id_{i}"}) for i, item in enumerate(sections)]
sections_data = {e["id"]: e["pattern"] for e in sections}
