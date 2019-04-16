
all: clean
	bookmanager proceedings.yml get --force
	cp dest/*.epub ..
	bookmanager proceedings.yml list

contrib:
	python ../bin/readme.py contrib 516 ../../.. > contributors.md
	git commit -m "upload contributors" contributors.md
	git push

clean:
	rm -rf dest

view:
	open ../*516*.epub