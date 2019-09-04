genmidi.lmp: config.py instruments/*
	./mkgenmidi $@
	cp $@ ../

clean:
	$(RM) genmidi.lmp ../genmidi.lmp *.pyc
	$(RM) __pycache__/*
	-rmdir __pycache__
