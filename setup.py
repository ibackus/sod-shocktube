import setuptools


setuptools.setup(
    name="sodshock",
    version="0.1.0",
    url="https://github.com/ibackus/sod-shocktube",
    author="Isaac Backus",
    description="A package which numerically solves the sod shock tube problem",
    long_description=open('README.md').read(),
    packages=setuptools.find_packages('src', exclude=['tests']),
    package_dir={"": "src"},
    install_requires=[
        'numpy >= 1.16',
        'matplotlib >= 2.2',
        'scipy >= 1.2',
        'python == 2.7.*',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)