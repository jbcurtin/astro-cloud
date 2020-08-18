release:
	pip install -U setuptools pip
	pip install -U twine
	make clean
	python setup.py sdist
	python -m twine upload --verbose dist/*

clean :
	rm -rf dist
	rm -rf build
	rm -rf astro_cloud.egg-info
	rm -rf .tox
    
install: clean
	pip uninstall astro-cloud
	python setup.py build
	python setup.py install

build-docs:
	pip install sphinx sphinx_rtd_theme pip setuptools -U
	mkdir -p /tmp/docs
	rm -rf /tmp/docs/*
	sphinx-build -b html docs/ /tmp/docs
