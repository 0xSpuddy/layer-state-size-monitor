from setuptools import setup, find_packages

setup(
    name="chain-size",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
    ],
    entry_points={
        'console_scripts': [
            'chain-size=chain_size:main',
        ],
    },
    author="Your Name",
    description="A tool to monitor and compare sizes of two directories",
    python_requires=">=3.6",
) 