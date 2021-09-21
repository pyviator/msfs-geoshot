SHELL = /bin/bash

install:
	poetry install

qtgui:
	python ./tools/build_ui.py

licenses:
	./tools/collect_licenses.sh

develop: qtgui licenses

build-standalone: qtgui licenses
	pyinstaller packaging/pyinstaller.spec

build-installer: qtgui licenses
	pynsist packaging/pynsist.cfg
