from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    package_list: List[str] = list()

    try:
        with open("requirements.txt", "r") as file:
            lines = file.readlines()

            for line in lines:
                package = line.strip()

                if package and package != "-e .":
                    package_list.append(package)
    except FileNotFoundError:
        print("requirements.txt file not found")

    return package_list


setup(
    name="ETL Pipeline Project",
    version="0.0.1",
    author="Serhat Karaman",
    author_email="serhatkaramanworkmail+support@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)

