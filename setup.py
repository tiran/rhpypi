import os

from setuptools import setup
from setuptools.command.build import build
from setuptools.command.install_lib import install_lib


PTH = "rhpypi-meta.pth"


class BuildPTH(build):
    def run(self):
        super().run()
        os.makedirs(self.build_lib, exist_ok=True)
        self.copy_file(PTH, os.path.join(self.build_lib, PTH))


class InstallLibPTH(install_lib):
    def run(self):
        super().run()
        self.__install_pth = os.path.join(self.install_dir, PTH)
        os.makedirs(self.install_dir, exist_ok=True)
        self.copy_file(PTH, self.__install_pth)

    def get_outputs(self):
        outputs = list(super().get_outputs())
        outputs.append(self.__install_pth)
        return outputs


setup(
    cmdclass={
        "build": BuildPTH,
        "install_lib": InstallLibPTH,
    },
)
