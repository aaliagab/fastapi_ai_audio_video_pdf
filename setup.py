from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='aiChat_audio_video_pdf_api',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
)

#pip install wheel
#python setup.py sdist bdist_wheel

