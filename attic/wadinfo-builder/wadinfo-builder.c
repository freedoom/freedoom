// -*- C++ -*-
//
// This reads the wadinfo.txt and outputs a new wadinfo.txt
// with the appropriate lines commented out for files which
// do not yet exist. This is so that wadinfo.txt can be
// automagically updated as we get more textures.
//
// This is also further proof that I need to learn perl.
//
// By Simon Howard (fraggle)
//

#include <stdio.h>
#include <string.h>
#include <dirent.h>

//
// check if a file exists in a subdirectory
// this ignores extension
// eg. if we do file_exists("flats", "ceil5_1")
// and a file flats/ceil5_1.gif exists it willl return 1
//

static int file_exists(char *dirname, char *filename)
{
	DIR *dir;
	struct dirent *direntry;
	
	dir = opendir(dirname);

	if(!dir) {
		fprintf(stderr, "cannot open dir: %s\n", dirname);
		exit(-1);
	}

	while(direntry = readdir(dir)) {
		if(!strncasecmp(direntry->d_name, filename, strlen(filename))
		   && direntry->d_name[strlen(filename)] == '.') {
			closedir(dir);
			return 1;
		}
	}
	
	closedir(dir);
	return 0;
}

int main(int argc, char *argv[])
{
	char *section = NULL;
	
	while(!feof(stdin)) {
		char buffer[128];
		char file[128];

		buffer[0] = '\0';
		
		fgets(buffer, 126, stdin);

		{
			char *p;
			for(p=buffer+strlen(buffer)-1; p >= buffer; p--) {
				if(isprint(*p))
					break;

				*p = '\0';
			}				
		}

		// comments and empty lines pass through
		
		if(buffer[0] == '#' || buffer[0] == '\0') {
			puts(buffer);
			continue;
		}

		// section header
		
		if(buffer[0] == '[') {
			if(section)
				free(section);

			section = strdup(buffer+1);
			
			*strchr(section, ']') = '\0';
			
			puts(buffer);

			if(!strcmp(section, "texture1") ||
			   !strcmp(section, "texture2")) {
				strcpy(section, "textures");
			}

			continue;
		}

		// copy first word of the buffer
		// into a second buffer

		{
			char *f, *b;
			for(b=buffer, f=file;
			    !isspace(*b) && *b;)
				*f++ = *b++;
			*f = '\0';
		}

		if(!section || file_exists(section, file)) {
			puts(buffer);
		} else {
			printf("#%s\n", buffer);
		}		
	}
}
