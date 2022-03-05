#!/usr/bin/env python


import os
from jinja2 import Environment, DictLoader, select_autoescape
import datetime
import sys
from git import Repo
import re

_changelog_template = """
## [{{tag}}] {{date}}

{% if added|length > 0 %}### Added
{% for v in added %}{{ v }}
{% endfor %}
{% endif %}{% if fixed|length > 0 %}### Fixed
{% for v in fixed %}{{ v }}
{% endfor %}
{% endif %}
"""
meta_template = """{% raw %}## [{{tag}}] {{date}}{% endraw %}

{% for e in entries %}{% raw %}{% if {% endraw %}{{e.id}}{% raw %}|length > 0 %}{% endraw %}{{e.output}}
{% raw %}{% for v in {% endraw %}{{e.id}}{% raw %} %}{{v}}
{% endfor %}
{% endif %}{% endraw %}{% endfor %}


"""

from release_notes import sections_data
from release_notes import sections as sect_raw


def create_release_notes(
    start_rev, tag_name, insertion_position, action, temporal_file_name
):
    if action == "generate":
        repo = Repo(".")

        for existing_tag in repo.tags:
            if existing_tag.name == tag_name:
                print(f"tag '{tag_name}' already exists")
                sys.exit(1)

        sections = {k: re.compile(v) for k, v in sections_data.items()}
        final_results = {k: [] for k, v in sections.items()}
        active = False
        if len(repo.tags) > 0:
            tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
            start_rev = tags[-1]

        rev = f"{start_rev}..HEAD"
        commits = repo.iter_commits(rev=rev)
        commits = list(commits)
        print(f"Processing {len(commits)} commits in the range: {rev}")
        if not len(commits) > 0:
            print("There are no commits to process, really?")
            sys.exit(1)
        for commit in commits:
            results = {k: [] for k, v in sections.items()}
            lines = commit.message.splitlines()
            for i in range(len(lines)):
                for k, v in sections.items():
                    if v.match(lines[i]):
                        active = k
                        continue
                if active:
                    if lines[i].strip() != "":
                        results[active].append(lines[i])
            for k, v in results.items():
                final_results[k] = final_results[k] + results[k][1:]
            active = False

        env0 = Environment(
            loader=DictLoader(
                {
                    "meta": meta_template,
                }
            ),
        )
        template2 = env0.get_template("meta")

        env = Environment(
            loader=DictLoader(
                {
                    "data": template2.render(entries=sect_raw),
                }
            ),
        )

        template = env.get_template("data")

        format_data = "%d/%m/%y"
        date = datetime.datetime.now().strftime(format_data)

        some = False
        for k, v in final_results.items():
            if len(v) > 0:
                some = True

        if not some:
            print("There is no release notes to add")
            sys.exit(1)

        release_notes = template.render(
            tag=tag_name, date=date, **final_results
        ).splitlines()
        open(temporal_file_name, "w").write("\n".join(release_notes))
    else:
        release_notes = open(temporal_file_name).read()
        os.remove(temporal_file_name)
        path = "CHANGELOG.md"
        if not os.path.exists(path):
            open(path, "w").write("# Changelog\n\n")

        changelog = list(open(path).readlines())
        changelog = (
            "".join(changelog[:insertion_position])
            + release_notes
            + "".join(changelog[insertion_position:])
        )

        open(path, "w").write(changelog)


def main():
    pos = int(os.getenv("CHANGELOG_INSERTION_POSITION", "2"))
    create_release_notes(
        start_rev=sys.argv[1],
        tag_name=sys.argv[2],
        insertion_position=pos,
        action=sys.argv[3],
        temporal_file_name=sys.argv[4],
    )
