
all : freedoom.lmp freedm.lmp misc-lumps genmidi-lump dmxgus.lmp \
      fd1txtr1.lmp fd2txtr1.lmp fdmtxtr1.lmp

misc-lumps:
	make -C cph/misc-lumps

genmidi-lump:
	make -C genmidi

dmxgus.lmp:
	make -C dmxgus

fd1txtr1.lmp fd2txtr1.lmp fdmtxtr1.lmp:
	make -C textures

freedoom.lmp: force
	echo $(VERSION) > freedoom.lmp

freedm.lmp: force
	echo $(VERSION) > freedm.lmp

force:

clean:
	make -C cph/misc-lumps clean
	make -C genmidi clean
	make -C dmxgus clean
	make -C textures clean

