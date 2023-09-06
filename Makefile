
setup_m1: 
	conda env create -f environment.m1.yaml
setup_ubuntu:
	conda env create -f environment.ubuntu.yaml
build:
	pip install --upgrade pip
	pip install -r requirements.txt

start:
	python app.py
