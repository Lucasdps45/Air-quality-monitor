from setuptools import setup, find_packages

setup(
    name="airquality",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.28.0",
        "psycopg2-binary>=2.9.0",
        "pandas>=1.5.0",
        "python-dotenv>=0.19.0"
    ]
)