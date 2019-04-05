from setuptools import setup, find_packages


with open('README.md') as f:
    long_description = f.read()

requirements = (
    'jinja2',
    'click',
    'watchdog',
    'pyyaml',
    'beautifulsoup4',
    'Pygments',
    'markdown',
)

setup(
    name='combine',
    version='0.0.17',
    description='A helpful, simple static site generator.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Dropseed',
    author_email='python@dropseed.io',
    python_requires='>=3.6.0',
    url='https://github.com/dropseed/combine',
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': ['combine=combine.cli:cli'],
    },
    install_requires=requirements,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
