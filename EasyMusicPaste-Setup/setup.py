from setuptools import setup, find_packages

setup(
    name='easy_music_paste',
    version='1',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['EMP=easy_music_paste.main:main']
    },
    install_requires=[
        'requests',
        'pyperclip'
    ]
)
