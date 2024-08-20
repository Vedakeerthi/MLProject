#This file is used to give my whole machine learning application as a package
from setuptools import find_packages,setup
from typing import List


HYPHEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    This function will get all the required packages from the requirement file
    '''
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        required_packages = [req.replace('\n','') for req in requirements]
        
        if HYPHEN_E_DOT in required_packages:
            required_packages.remove(HYPHEN_E_DOT)
    
    return required_packages
    
setup(
    name='mlproject',version='0.1', author='Vedakeerthi',
    author_email='vedakeerthi2002@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)