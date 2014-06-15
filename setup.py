from setuptools import setup, find_packages

setup(name='sampleapp',
      version='1.0',
      url='https://github.com/jwmatthews/python_flask_mongoengine_restapi',
      description='Sample REST API using Flask and Mongoengine',
      license='GPLv2',

      author='John Matthews',
      author_email='jwmatthews@gmail.com',

      packages=find_packages(),
      test_suite='nose.collector',

      classifiers=['Intended Audience :: Developers',
                   'Intended Audience :: Information Technology',
                   'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                   'Operating System :: POSIX',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Software Development :: Libraries :: Python Modules',],

      options={'build': {'build_base': '_build'},
               'sdist': {'dist_dir': '_dist'},},

      install_requires=[],)
