from setuptools import setup, find_packages

setup(
    name='JJCale',
    version='0.1',
    description='a simple web framework',
    long_description='a simple web framework',
    url='https://github.com/lrhhhhhh/JJCale',
    author='lrhaoo',
    license='MIT',
    keywords=('web', 'framework'),
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'Werkzeug>=2.0.0',
        'jinja2>=3.0.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
