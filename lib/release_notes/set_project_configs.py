#!/usr/bin/env python

import os
from release_notes import k8s_data, data
import random

template_data = """
{
  "k8s-configs": [
  {% for path in items %}
    {
      "file_path": "{{ path }}/deploy.yml",
      "yaml_path": "select(.kind == \\"Deployment\\").spec.template.spec.containers.0.image"
    } {{ "," if not loop.last }}
{% endfor %}
],
"sname" : "{{sname}}",
"cookie" : "{{cookie}}"
}
"""
from importlib.resources import files

from jinja2 import Environment, DictLoader, select_autoescape


def main():
    global template_data
    folder = ".rdev-configs"
    config_file = f"{folder}/configs.json"
    if not os.path.exists(config_file):
        env = Environment(
            loader=DictLoader(
                {
                    "data": template_data,
                }
            ),
        )
        template = env.get_template("data")
        items = [
            f"{k8s_data['path']}/{f}"
            for f in os.listdir(k8s_data["path"])
            if os.path.isdir(f"{k8s_data['path']}/{f}")
            and f.startswith(k8s_data["dir-prefix"])
        ]
        value = template.render(
            items=items,
            sname=f"node-{random.randint(1, 100)}",
            cookie=f"cookie-{random.randint(1, 100)}",
        )
        if not os.path.exists(folder):
            os.makedirs(folder)
        open(config_file, "w").write(value)
    cli_folder = "cli"
    if not os.path.exists(cli_folder):
        os.makedirs(cli_folder)
    script = files(data).joinpath("srv").read_text()
    open(f"{cli_folder}/srv", "w").write(script)
