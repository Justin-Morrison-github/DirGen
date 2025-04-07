from setuptools import setup


setup(
    name="dirgen",
    version="0.1",
    package_dir={"": "src"},  # Root package is in the "src" folder
    py_modules=["dirgen"],     # Refers to src/dirgen.py
    entry_points={
        'console_scripts': [
            'dirgen=dirgen:main',
        ],
    },
)
