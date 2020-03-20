from setuptools import find_packages, setup

setup(
    name="mqtt_client",
    version="1.0.0",
    author="Andrew Robbertz",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["paho-mqtt", "argparse"],
)
