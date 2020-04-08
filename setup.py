from setuptools import find_packages, setup

setup(
      name='robotframework-historic-parser',
      version="0.1.8",
      description='Parser to push robotframework execution results to MySQL',
      classifiers=[
          'Framework :: Robot Framework',
          'Programming Language :: Python',
          'Topic :: Software Development :: Testing',
      ],
      keywords='robotframework historical execution report parser',
      author='Shiva Prasad Adirala',
      author_email='adiralashiva8@gmail.com',
      url='https://github.com/adiralashiva8/robotframework-historic-parser',
      license='MIT',

      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'robotframework',
          'mysql-connector',
      ],
      entry_points={
          'console_scripts': [
              'rfhistoricparser=robotframework_historic_parser.runner:main',
          ]
      },
)