MODULES = binfilepy myutil xmlconvert

all:
	pyinstaller --onefile src/wfconvert.py
	cp ./src/wfconvert_config.yaml ./dist/
	pyinstaller --onefile src/wfshow.py

wfconvert:
	pyinstaller --onefile src/wfconvert.py
	cp ./src/wfconvert_config.yaml ./dist/

wfshow:
	pyinstaller --onefile src/wfshow.py

# requirements.txt is generated by
# pipreqs .
init:
	pip install -r requirements.txt

clean:
	rm -rf ./.cache ./__pycache__ ./.pytest_cache
	rm -rf ./src/.cache ./src/__pycache__
	rm -rf ./tests/.cache ./tests/__pycache__
	rm -rf $(foreach var,$(MODULES), ./src/$(var)/__pycache__)
	rm -rf $(foreach var,$(MODULES), ./src/$(var)/.cache)
	rm -rf ./build
	rm -rf ./dist

pep8:
	pep8 .

autopep8:
	autopep8 . --recursive --in-place --pep8-passes 2000

lint:
	make pep8

lint-fix:
	make autopep8

test:
	py.test . --verbose

test_parsetime:
	pytest ./tests/test_myutil.py -k test_parsetime -s
