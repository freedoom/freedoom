CPP=../../scripts/simplecpp

all: ../fdmwdinf.lmp ../p1_wdinf.lmp ../p2_wdinf.lmp

../fdmwdinf.lmp: wadinfo.txt
	$(CPP) -DFREEDM < $< > $@

../p1_wdinf.lmp: wadinfo.txt
	$(CPP) -DPHASE1 < $< > $@

../p2_wdinf.lmp: wadinfo.txt
	$(CPP) -DPHASE2 < $< > $@

clean:
	$(RM) ../fdmwdinf.lmp ../p1_wdinf.lmp ../p2_wdinf.lmp
