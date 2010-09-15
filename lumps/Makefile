
all : freedoom.lmp freedm.lmp misc-lumps

misc-lumps:
	make -C cph/misc-lumps

freedoom.lmp: force
	echo $(VERSION) > freedoom.lmp

freedm.lmp: force
	echo $(VERSION) > freedm.lmp

force:

clean:
	make -C cph/misc-lumps clean
