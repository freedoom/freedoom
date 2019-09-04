ultramid.ini : gen-ultramid config.py stats.py
	./gen-ultramid $@
	cp $@ ../dmxgus.lmp

clean:
	$(RM) ultramid.ini ../dmxgus.lmp *.pyc
	$(RM) __pycache__/*
	-rmdir __pycache__
