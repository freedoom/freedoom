#include <stdio.h>
#include <stdlib.h>

void print_byte(int i)
{
	unsigned char c = i;

	printf("%c", c);
}

int main(int argc, char *argv[])
{
	// header

	print_byte(109);	// version
	print_byte(0);		// skill
	print_byte(1);		// episode
	print_byte(1);		// level
	print_byte(0);		// mode (single/coop)
	print_byte(0);		// respawn
	print_byte(0);		// fast monsters
	print_byte(0);		// nomonsters
	print_byte(0);		// viewpoint
	print_byte(1);		// player 1 present
	print_byte(0);		// player 2 present
	print_byte(0);		// player 3 present
	print_byte(0);		// player 4 present

	// one frame and then quit
	
	print_byte(0);
	print_byte(0);
	print_byte(0);
	print_byte(0);
	
	// end of demo

	print_byte(0x80);	// end of demo
}

