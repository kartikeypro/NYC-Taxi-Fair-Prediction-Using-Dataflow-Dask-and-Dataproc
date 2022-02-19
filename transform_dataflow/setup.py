import setuptools

PACKAGE_NAME = 'nyc_data_transformation'
PACKAGE_VERSION='0.0.1'

setuptools.setup (
name=PACKAGE_NAME,
version=PACKAGE_VERSION,
description='Running python on dataflow.',
install_requires=[
    'apache-beam',
    'apache-beam[gcp]'
],
packages=setuptools.find_packages(),
package_data={PACKAGE_NAME: [
    "data/*.log"]}
)