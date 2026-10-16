from setuptools import setup, find_packages #type: ignore
from typing import List

def get_requirements()->List[str]:
    """
    This function will return list of requirements.
    """
    requirements_list : List[str] = []
    try:
        with open("requirements.txt" , "r") as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()

                if requirement and requirement !="-e .":
                    requirements_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found.")

    return requirements_list


print(get_requirements())

setup(
    name = "NetworkSecurityProject",
    version = "0.0.1",
    author = "Abhimanyu Singh",
    author_email = "abhimanyustomar24@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)


                    