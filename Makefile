version := 0.1.1-dev0


clean-dist:
	rm -rf dist/

build-wheel: clean-dist build-requirements
	python setup.py sdist bdist_wheel

publish: build-wheel
	twine upload --repository pypi dist/*

test-publish: build-wheel
	twine upload --repository testpypi dist/*

dev-requirements:
	pip install -r requirements.txt

build-requirements:
	pip install -r build-requirements.txt

tox-requirements:
	pip install -r tox-requirements.txt

install-dev: build-wheel
	pip install dist/*.whl

build-test: install-dev
	pytest -vvs tests/

full-test: build-test
	tox --parallel
