version := 0.1.1-dev0

build-wheel:
	python setup.py sdist bdist_wheel
	twine check dist/*

publish: build-wheel
	twine upload --repository pypi dist/*

test-publish: build-wheel
	twine upload --repository testpypi dist/*
