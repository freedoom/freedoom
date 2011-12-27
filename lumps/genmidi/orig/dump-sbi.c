//
// Copyright (c) 2011, Simon Howard
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
//  * Redistributions of source code must retain the above copyright notice,
//    this list of conditions and the following disclaimer.
//  * Redistributions in binary form must reproduce the above copyright
//    notice, this list of conditions and the following disclaimer in the
//    documentation and/or other materials provided with the distribution.
//  * Neither the name of Freedoom project nor the names of its contributors
//    may be used to endorse or promote products derived from this software
//    without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "oplvar.h"

#define SBI_HEADER "SBI\x1a"

struct sbi {
	char header[4];
	char name[32];
	char opldata[16];
};

extern char *genmidi_instr_names[];

static int is_null_instr(struct opl_operators *instrument)
{
	int i;

	for (i = 0; i < 10; ++i) {
		if (instrument->ops[i] != 0x00) {
			return 0;
		}
	}

	return 1;
}

static void write_sbi(char *filename, char *instrname, struct opl_operators *opl)
{
	FILE *fs;
	struct sbi data;

	memset(&data, 0, sizeof(data));
	memcpy(data.header, SBI_HEADER, 4);
	strcpy(data.name, instrname);
	memcpy(data.opldata, opl->ops, 16);

	fs = fopen(filename, "wb");
	fwrite(&data, 1, sizeof(data), fs);
	fclose(fs);
}

int main(int argc, char *argv[])
{
	char filename[32];
	int i;

	for (i = 0; i < 175; ++i) {
		if (is_null_instr(&opl2_instrs[i])) {
			continue;
		}

		if (i < 128) {
			sprintf(filename, "instr%03i.sbi", i + 1);
		} else {
			sprintf(filename, "perc%02i.sbi", i - 128 + 35);
		}

		write_sbi(filename, genmidi_instr_names[i], &opl2_instrs[i]);
	}

	return 0;
}

