
all: clean
	bookmanager proceedings.yml get --force
	cp dest/*.epub ..
	bookmanager proceedings.yml list

projects:
	python ../bin/readme.py projects 516 ../../.. > projects.md
	git commit -m "upload project list" projects.md
	git push

contrib:
	python ../bin/readme.py contrib 516 ../../.. > contributors.md
	git commit -m "upload contributors" contributors.md
	git push

clean:
	rm -rf dest

view:
	open ../*516*.epub