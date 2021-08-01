SRC_DIR='src'
TEMP_PACKAGE_DIR='chat_analyzer'

build: prepare_package_dir build_package remove_package_dir

install: prepare_package_dir install_package remove_package_dir

clean_package:
	rm -r dist || echo 'dist removed'
	rm -r ${SRC_DIR}/${TEMP_PACKAGE_DIR}.egg-info || echo 'egg-info removed'

build_package:
	python -m build

install_package:
	pip install .

prepare_package_dir:
	mkdir ${TEMP_PACKAGE_DIR}
	cp -R ${SRC_DIR}/* ${TEMP_PACKAGE_DIR}/
	mv ${TEMP_PACKAGE_DIR} ${SRC_DIR}/${TEMP_PACKAGE_DIR}

remove_package_dir:
	rm -rf ${SRC_DIR}/${TEMP_PACKAGE_DIR}
