from setuptools import setup

package_name = 'yunji_ros_driver'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='bibtv',
    maintainer_email='alan@example.com',
    description='ROS2 driver for Yunji robots with PoseMesh integration',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'yunji_node = ' + package_name + '.yunji_node:main',
        ],
    },
)
