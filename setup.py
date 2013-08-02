from distutils import setup

setup(
    name="pyprol",
    version="0.1.0",
    description="Python Performance Measure System",
    author="Stefan Koenen",
    author_email="stefan.koenen@uni-duesseldorf.de",
    url="https://github.com/skoenen/pyprol",
    packages=['pyprol'],
    entry_points={'paste.app_factory': ['main=pyprol.inject']},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Environment :: Server',
        'Intended Audience :: Developer',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Topic :: Software Development :: Profiling'
        ],
    install_requires=[
        'yappi ==0.62',
        'sqlalchemy ==0.8'
        ]
    )
