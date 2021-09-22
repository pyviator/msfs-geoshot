SHELL = /bin/bash
PROJECT = msfs_geoshot

install:
	poetry install

qtgui:
	python ./tools/build_ui.py

licenses:
	./tools/collect_licenses.sh

check:
	python -m mypy $(PROJECT)
	python -m flake8 $(PROJECT)
	python -m black --check $(PROJECT)

develop: qtgui licenses

run: develop
	python -m $(PROJECT)

pynsist-config:
	./tools/build_pynsist_config.py

build-standalone: qtgui licenses
	pyinstaller packaging/pyinstaller.spec

build-installer: qtgui licenses pynsist-config
	pynsist packaging/pynsist.cfg
