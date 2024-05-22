from importlib.machinery import SourceFileLoader, PathFinder
import platform
import sys
import types
import typing


class RhPyPILoader(SourceFileLoader):
    def get_os_tag(self) -> str:
        osrelease = platform.freedesktop_os_release()
        osid = osrelease["ID"]
        if osid == "fedora":
            return f"fc{osrelease['VERSION_ID']}"
        raise ValueError(osid)

    def exec_module(self, module: types.ModuleType) -> None:
        super().exec_module(module)

        module._orig_platform_tags = module.platform_tags

        os_tag = self.get_os_tag()
        machine = platform.machine()

        def rhpypi_platform_tags() -> typing.Iterator[str]:
            yield f"{os_tag}-{machine}-cu12"
            yield f"{os_tag}-{machine}"
            yield from module._orig_platform_tags()

        module.platform_tags = rhpypi_platform_tags


class RhPyPIMetaImporter:

    modules = {
        "packaging.tags",
        "pipenv.patched.pip._vendor.packaging.tags",
        "pip._vendor.packaging.tags",
        "pkg_resources._vendor.packaging.tags",
        "setuptools._vendor.packaging.tags",
        "wheel.vendored.packaging.tags",
    }

    def find_spec(self, fullname: str, path=None, target=None):
        if fullname in self.modules:
            spec = PathFinder.find_spec(fullname, path)
            if spec is not None and isinstance(spec.loader, SourceFileLoader):
                spec.loader = RhPyPILoader(spec.loader.name, spec.loader.path)
                return spec
        return None


meta_importer = RhPyPIMetaImporter()

sys.meta_path.insert(1, meta_importer)
