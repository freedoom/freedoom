ultramid.ini : gen-ultramid config.py stats.py
	./gen-ultramid $@
	cp $@ ../dmxgus.lmp

clean:
	rm -f ultramid.ini ../dmxgus.lmp *.pyc
	rm -fr __pycache__
