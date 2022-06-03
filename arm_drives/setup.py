# coding=utf-8
from setuptools import setup

setup(
    author="HaoranYin",
    author_email ="h.yin@umail.leidenuniv.nl",
    description="Drivers for Grab-it and MotoPi, chip is PCA9685.",
    url="",
    name="arm_drives",
    version="1.0",
    packages=['.'],
    install_requires=[
        "smbus"
                     ],
    exclude_package_date={'':['.gitignore'], '':['__pycache__'], '':['dist'],
                          '':'build', '':'PCA9685_Driver.egg.info',
                          '':'arm_drivers.egg.info', '':'arm_drives.egg.info'},
)
