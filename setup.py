from setuptools import setup, find_packages

setup(
    name='xleb',
    version='1.4',
    py_modules=['xleb'],
    packages=['xleb'],
    description='web-based remote file manager',
    url='https://git.pegasko.art/pegasko/xleb',
    author_email='pegasko@pegasko.art',
    license='AGPL 3.0',
    keywords='web-based file-manager remote-access',
    package_data={
        'xleb': [
            'static/**',
        ]
    },
    entry_points={
        'console_scripts': [
            'xleb = xleb.__main__:main'
        ]
    },
    include_package_data=True,
    install_requires=[
        'aiohttp',
        'aiohttp-middlewares',
    ],
)
