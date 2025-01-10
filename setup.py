from setuptools import setup, find_packages

setup(
    name="nova",
    version="1.0.0",
    description="A terminal-based interactive CLI tool for AWS RDS backup management",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/nova",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "boto3>=1.28.0",
        "rich>=13.4.0",
        "prompt_toolkit>=3.0.39",
        "pandas>=2.1.0",
    ],
    entry_points={
        "console_scripts": [
            "nova=nova.cli:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    include_package_data=True,
)
