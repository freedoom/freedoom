
CFLAGS = -Wall
OBJS = oplinstrs.o instrnames.o

genmidi.lmp : genmidi-gen
	./genmidi-gen $@

genmidi-gen : $(OBJS) genmidi-gen.o
	$(CC) $(LDFLAGS) $(OBJS) genmidi-gen.o -o $@

dump-sbi : $(OBJS) dump-sbi.o
	$(CC) $(LDFLAGS) $(OBJS) dump-sbi.o -o $@

%.o : %.c
	$(CC) $(CFLAGS) -c $^ -o $@

clean:
	rm -f $(OBJS) genmidi-gen genmidi.lmp

