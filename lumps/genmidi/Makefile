genmidi.lmp: config.py instruments/*
	./mkgenmidi $@
	cp $@ ../

clean:
	rm -f genmidi.lmp ../genmidi.lmp *.pyc
	rm -fr __pycache__
