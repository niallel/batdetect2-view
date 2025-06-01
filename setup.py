from setuptools import setup, find_packages

setup(
    name="batdetect2-view",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "argparse",
    ],
    entry_points={
        'console_scripts': [
            'batdetect2-view=batdetect2_view:main',
        ],
    },
    author="Niall",
    description="A visualization tool for batdetect2 output files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/batdetect2-view",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 