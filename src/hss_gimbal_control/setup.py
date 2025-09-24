from setuptools import setup

package_name = 'hss_gimbal_control'

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
    description='ROS 2 package for controlling the HSS gimbal',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gimbal_control_node = hss_gimbal_control.gimbal_control_node:main',
        ],
    },
)
