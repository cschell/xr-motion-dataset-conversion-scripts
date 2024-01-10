from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

print(find_packages())

setup(
    name='motion_dataset_converter',
    version='0.1.0',
    packages=find_packages(),
    description='The #1 motion dataset conversion tool!!',
    long_description=open('README.md').read(),
    install_requires=requirements,
    python_requires='>=3.6',
)
