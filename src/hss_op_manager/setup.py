from setuptools import setup

package_name = 'hss_op_manager'

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
    description='ROS 2 package for managing HSS operations and modes',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'operation_manager_node = hss_op_manager.operation_manager_node:main',
        ],
    },
)
