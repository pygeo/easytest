

clean :
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -name "y.pkl" -exec rm -rf {} \;
	find . -name "*.so" -exec rm -rf {} \;
	find . -name "data_warnings.log" -exec rm -rf {} \;
	rm -rf C:*debuglog.txt
	rm -rf build
	rm -rf MANIFEST
	rm -rf cover
	rm -rf tmp
	rm -rf doc
	rm -rf dist
	rm -rf pycmbs.egg-info

dist : clean
	python setup.py sdist

update_version:
	python autoincrement_version.py

upload_pip: update_version
	# ensure that pip version has always counterpart on github
	git push origin master
	# note that this requres .pypirc file beeing in home directory
	python setup.py sdist upload
