import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tp-link-controller",
    version="0.0.1",
    author="Mohamed Farhan Fazal",
    author_email="fazal.farhan@gmail.com",
    description="A Python Package to controll TP-Link Routers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fazalfarhan01/TP-Link-Router-Controller",
    install_requires=[
        "colorama",
        "selenium",
        "browsermob-proxy"
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)