import setuptools
import pathlib
import sys

from setuptools import find_packages

here = pathlib.Path(__file__).parent.resolve()

install_requires = (
    (here / "requirements/common.txt").read_text(encoding="utf-8").splitlines()
)

from setuptools.command.install import install


class PostInstallCommand(install):
    def run(self):
        import os

        CONFIG_PATH = f"{os.getenv('HOME')}/.rdev"
        if not os.path.exists(CONFIG_PATH):
            os.makedirs(CONFIG_PATH)
        config_file_path = f"{CONFIG_PATH}/configs.json"
        if not os.path.exists(config_file_path):
            open(config_file_path, "w").write(
                (here / "configs/configs.json").read_text(encoding="utf-8")
            )
        install.run(self)


setuptools.setup(
    name="release_notes",
    version="0.0.1",
    author="J. Albert Cruz",
    author_email="jalbertcruz@gmail.com",
    license="MIT",
    package_dir={
        "": "lib",
    },
    packages=find_packages("lib"),
    install_requires=install_requires,
    include_package_data=True,
    scripts=[
        "bin/create-tag",
        "bin/set-lppush",
        "bin/r-exp",
        "bin/r-iex",
        "bin/set-lconfigs",
    ],
    entry_points={
        "console_scripts": [
            "_rdev=release_notes.generator:main",
            "_pre_push=release_notes.pre_push:put_as_pre_push_githook",
            "_set_pconfigs=release_notes.set_project_configs:main",
        ],
    },
    cmdclass={
        "install": PostInstallCommand,
    },
    # data_files=[('configs/rdev', ['configs/config.json'])],
)
