from setuptools import setup


setup(
    name="mytool",
    version="0.1",
    package_dir={"": "src"},  # Root package is in the "src" folder
    py_modules=["mytool"],     # Refers to src/mytool.py
    entry_points={
        'console_scripts': [
            'mytool=mytool:main',
        ],
    },
)
