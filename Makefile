SHELL = /bin/bash

install:
	poetry install

qtgui:
	python ./tools/build_ui.py

licenses:
	./tools/collect_licenses.sh

develop: qtgui licenses

pynsist-config:
	./tools/build_pynsist_config.py

build-standalone: qtgui licenses
	pyinstaller packaging/pyinstaller.spec

build-installer: qtgui licenses pynsist-config
	pynsist packaging/pynsist.cfg
