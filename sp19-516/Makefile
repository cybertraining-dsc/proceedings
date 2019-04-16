
all: clean
	bookmanager proceedings.yml get --force
	cp dest/*.epub ..
	bookmanager proceedings.yml list

contrib:
	python ../bin/readme.py contrib 516 ../../.. > contributors.md
	git commit -m "upload contributors" contributors.md
	git push contributors.md

clean:
	rm -rf dest