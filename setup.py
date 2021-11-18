import setuptools


setuptools.setup(
    name="sodshock",
    version="0.1.9",
    url="https://github.com/ibackus/sod-shocktube",
    author="Isaac Backus",
    description="A package which numerically solves the sod shock tube problem",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages('src', exclude=['tests']),
    package_dir={"": "src"},
    install_requires=[
        'numpy >= 1.3.0',
        'matplotlib >= 2.0.0',
        'scipy >= 1.0.0',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
