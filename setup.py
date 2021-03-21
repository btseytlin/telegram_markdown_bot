import setuptools

with open('requirements.txt') as req_file:
    requirements = req_file.read().splitlines()

setuptools.setup(
    name='tgmarkdown',
    version='0.0.1',
    url='https://github.com/btseytlin/telegram_markdown_bot',
    author='tg:@boris_again',
    author_email='b.tseytlin@lambda-it.ru',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
    python_requires=">=3.6"
)
