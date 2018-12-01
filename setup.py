from setuptools import setup, find_packages

setup(
    name='gossip',
    version="0.1.0",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'gossip = gossip.prettyfy:main',
            'gossip_fetch = gossip.fetch:main'
        ]
    }
)
