
CFLAGS = -Wall
OBJS = genmidi-gen.o oplinstrs.o instrnames.o

genmidi.lmp : genmidi-gen
	./genmidi-gen $@

genmidi-gen : $(OBJS)
	$(CC) $(LDFLAGS) $(OBJS) -o $@

%.o : %.c
	$(CC) $(CFLAGS) -c $^ -o $@

clean:
	rm -f $(OBJS) genmidi-gen genmidi.lmp

