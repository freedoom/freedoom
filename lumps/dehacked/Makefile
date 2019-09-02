CPP=../../scripts/simplecpp

all: ../fdm_deh.lmp ../p1_deh.lmp ../p2_deh.lmp

../fdm_deh.lmp: dehacked.txt
	$(CPP) -DFREEDM < $< > $@

../p1_deh.lmp: dehacked.txt
	$(CPP) -DPHASE1 < $< > $@

../p2_deh.lmp: dehacked.txt
	$(CPP) -DPHASE2 < $< > $@

clean:
	$(RM) ../fdm_deh.lmp ../p1_deh.lmp ../p2_deh.lmp
