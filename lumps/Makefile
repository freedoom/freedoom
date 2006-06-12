
all : freedoom.lmp misc-lumps

misc-lumps:
	make -C cph/misc-lumps

freedoom.lmp: force
	echo $(VERSION) > freedoom.lmp

force:

clean:
	make -C cph/misc-lumps clean
