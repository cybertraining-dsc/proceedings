
epub: clean
	bookmanager proceedings.yml get --force
	cp dest/*.epub ..
	bookmanager proceedings.yml list

artifacts: projects contrib sections chapters push
	echo done

push:
	git commit -m "upload project list" projects.md
	git commit -m "upload contributors" contributors.md
	git commit -m "upload section list" sections.md
	git commit -m "upload chapters list" chapters.md
	git push

projects:
	python ../bin/readme.py projects 516 ../../.. > projects.md

contrib:
	python ../bin/readme.py contrib 516 ../../.. > contributors.md

sections:
	python ../bin/readme.py sections 516 ../../.. > sections.md

chapters:
	python ../bin/readme.py chapters 516 ../../.. > chapters.md

#> chapters.md
#	git commit -m "upload chapters list" projects.md
#	git push



clean:
	rm -rf dest

view:
	open ../*516*.epub