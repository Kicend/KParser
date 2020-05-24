from setuptools import setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name='KParser',
    version='0.7.2',
    packages=[],
    install_requires=requirements,
    url='https://github.com/Kicend/KParser',
    license='MIT',
    author='Filip "Kicend" Szczepanowski',
    author_email='kicend@gmail.com',
    description='Get e-mail addresses from websites'
)

