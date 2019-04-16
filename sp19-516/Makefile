EPUB=`fgrep "filename:" proceedings.yml | sed "s/\"//g" | sed 's/filename: //'`


all: clean
	bookmanager proceedings.yml get --force
	cp dest/$(EPUB) ..

clean:
	rm -rf dest