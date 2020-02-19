from setuptools import setup, find_packages

requires = [
    'SQLAlchemy==1.3.13',
    'psycopg2-binary==2.8.4',
]

setup(
    name='bankzero',
    version='1.0.0',
    author='',
    author_email='',
    url='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
)
