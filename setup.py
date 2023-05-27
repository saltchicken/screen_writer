import setuptools

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

setuptools.setup(
    name='screen_writer',
    version='0.0.18',
    author='John Eicher',
    author_email='john.eicher89@gmail.com',
    description='Testing installation of Package',
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url='https://github.com/saltchicken/screen_writer',
    # project_urls = {
    #     "Bug Tracker": "https://github.com/saltchicken/screen_writer/issues"
    # },
    # license='MIT',
    py_modules=['screen_writer'],
    install_requires=['pyqt5'],
)
