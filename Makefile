SHELL = /bin/bash

install:
	poetry install

qtgui:
	python ./tools/build_ui.py

licenses:
	./tools/collect_licenses.sh

develop: qtgui licenses

build: qtgui licenses
	pyinstaller app.spec
