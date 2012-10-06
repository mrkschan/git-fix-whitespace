import os

from setuptools import setup, find_packages


desc = 'Fix whitespace problem according to git-config'
__version__ = ('0', '1', '0')

cwd = os.path.abspath(os.path.dirname(__file__))


def pip_requirements():
    '''Return non-comment lines from requirements.txt'''
    with open(os.path.join(cwd, 'requirements.txt'), 'r') as f:
        lines = filter(None, [i.strip() for i in f.readlines()])

    requirements = [i for i in lines if i[0] != '#']
    return requirements


setup(
    name='git-fix-whitespace',
    version='.'.join(__version__),
    description=desc,
    author='mrkschan',
    author_email='mrkschan@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'git-fix-whitespace = git_fix_whitespace.git_fix_whitespace:main',
        ]
    },
    install_requires=pip_requirements(),
)
