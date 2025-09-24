from setuptools import setup

package_name = 'hss_gui'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='tayfurcnr@gmail.com',
    description='ROS 2 package for the HSS Ground Station Interface',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ground_station_node = hss_gui.ground_station_node:main',
        ],
    },
)
