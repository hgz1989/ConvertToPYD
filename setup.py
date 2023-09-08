from distutils.core import setup, Extension
from glob import glob
from importlib.util import find_spec
from pathlib import Path
from shutil import rmtree

from Cython.Build import cythonize


def delete_file(package_name: str, filename: str = "*.c") -> None:
    """
    删除文件
    :param package_name:包名(转换跟目录的直接输入一个.)
    :param filename:文件名(带后缀,如果删除同一类型的就用*.后缀名)
    :return:None
    """
    for module_path in glob(f"{package_name}/{filename}"):
        filepath = Path(__file__).parent / module_path
        print(filepath)
        if filepath.exists() and filepath.is_file():
            filepath.unlink()


def convert_to_pyd(package_name: str, filename: str = "*.py") -> None:
    """
    将代码转为pyd文件
    :param package_name:包名(转换跟目录的直接输入一个.)
    :param filename:
    :return:文件名(带后缀,如果转换同一类型的就用*.后缀名)
    """
    extensions = []
    for module_path in glob(f"{package_name}/{filename}"):
        if package_name == ".":
            extension = module_path[2:]
        else:
            module_name = module_path[:-3].replace("\\", ".")
            if module_name.endswith(("__init__.py", "setup.py")):
                continue
            extension = Extension(module_name, sources=[module_path])
        extensions.append(extension)
    setup(name=pkg_name, ext_modules=cythonize(extensions))
    rmtree("build")


if __name__ == "__main__":
    for i in range(5):
        pkg_name = input(f"请输入需要转换成pyd的包名或模块名[{i + 1}]：")
        if pkg_name == ".":
            break
        spec = find_spec(pkg_name)
        if spec:
            break
    else:
        raise ValueError("连续五次输入模块错误，请检查好后再试!")
    delete_file(pkg_name, "*.pyd")
    delete_file(pkg_name)
    convert_to_pyd(pkg_name)
    delete_file(pkg_name)
