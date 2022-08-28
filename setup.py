# =========================================================================
from pkg_resources import parse_requirements as pk_parse_requirements
from pathlib import Path
from setuptools import setup, find_packages
# =========================================================================
name = 'iptoolbox'
version = '0.0.2'
# =========================================================================


BASE_DIR = Path(__file__).resolve().parent


# If you make changes to the project and the changes require other packages that are available in pypi, put them in the "requirements.txt" file.
if not Path(BASE_DIR / "requirements.txt").is_file():
    print(
        "\n"
        "There is no 'requirements.txt' file."
        "\n"
        "\tGet the content of the file from the link below"
        "\n\n"
        f">> [https://github.com/V70024/{name}/blob/{version}/requirements.txt]"
        "\n\n"
    )
    exit()


with open(BASE_DIR / "requirements.txt", "r") as requirements_txt:
    reqs = [str(requirement) for requirement in pk_parse_requirements(requirements_txt)]

with open(BASE_DIR / "README.md", 'r') as file_README:
    long_description = file_README.read()


classifiers = [
    "Topic :: Internet",

    "Natural Language :: English",

    "License :: OSI Approved :: MIT License",

    "Development Status :: 1 - Planning",

    "Operating System :: POSIX",
    "Operating System :: Unix",
    "Operating System :: Microsoft",
    "Operating System :: MacOS",
    "Operating System :: BeOS",

    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
]


project_urls = {
    'Repository': f'https://github.com/V70024/iptoolbox/tree/{version}',
    'Documentation': f'https://github.com/V70024/iptoolbox/wiki/iptoolbox-{version}',
    'Bug Tracker': 'https://github.com/V70024/iptoolbox/issues'
}


setup(
    name=name,
    version=version,
    description=f'{name} is a tool for purposefully creating IP, testing and scanning it',
    author='V70024',
    author_email='Zz2f0024@protonmail.com',
    python_requires='>=3.6',
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls=project_urls,
    url=f'https://github.com/V70024/{name}',
    classifiers=classifiers,
    package_data={name: ['data.json']},
    keywords=name,
    packages=find_packages(),
    install_requires=reqs
)
