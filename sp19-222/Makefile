
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
	git pushgit add pro

projects:
	python ../bin/readme.py projects 222 ../../.. > projects.md

contrib:
	python ../bin/readme.py contrib 222 ../../.. > contributors.md

sections:
	python ../bin/readme.py sections 222 ../../.. > sections.md

chapters:
	python ../bin/readme.py chapters 222 ../../.. > chapters.md

#> chapters.md
#	git commit -m "upload chapters list" projects.md
#	git push



clean:
	rm -rf dest

view:
	open ../*222*.epub