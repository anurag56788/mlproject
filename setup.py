from setuptools import find_packages,setup
from typing import List

HYPHEN_E_DOT= "-e ."

def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirement
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=[req.strip() for req in file_obj.readlines()]
        requirements=[req for req in requirements if req and not req.startswith('#')]
        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements





setup(
name ='mlproject',
version='0.0.1',
author='Anurag',
author_email="anuragyadav001.73@gmail.com",
packages=find_packages(),
install_requires=get_requirements('requirements.txt')



)