// 
// Copyright (c) 2007, Simon Howard 
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

#define HEADER_DATA "#OPL_II#"
#define NUM_BASIC_INSTRUMENTS 128
#define NUM_INSTRUMENTS 175

#define FL_FIXED_PITCH  0x0001          // note has fixed pitch (see below)
#define FL_DOUBLE_VOICE 0x0004          // use two voices instead of one

// Mask for splitting keyscale / output level.  Although in SBI they are
// contained within the same byte, for some reason they are split into
// two separate bytes in the GENMIDI lump.

#define KEYSCALE_MASK   0xc0

extern char *genmidi_instr_names[];

static void write_header(FILE *fstream)
{
        fwrite(HEADER_DATA, 1, strlen(HEADER_DATA), fstream);
}

static void write_sbi_data(FILE *fstream, unsigned char *data)
{
        // Modulator

        fputc(data[OO_CHARS], fstream);
        fputc(data[OO_ATT_DEC], fstream);
        fputc(data[OO_SUS_REL], fstream);
        fputc(data[OO_WAV_SEL], fstream);
        fputc(data[OO_KSL_LEV] & KEYSCALE_MASK, fstream);
        fputc(data[OO_KSL_LEV] & ~KEYSCALE_MASK, fstream);

        // Feedback (both channels)

        fputc(data[OO_FB_CONN], fstream);

        // Carrier

        fputc(data[OO_CHARS + 1], fstream);
        fputc(data[OO_ATT_DEC + 1], fstream);
        fputc(data[OO_SUS_REL + 1], fstream);
        fputc(data[OO_WAV_SEL + 1], fstream);
        fputc(data[OO_KSL_LEV + 1] & KEYSCALE_MASK, fstream);
        fputc(data[OO_KSL_LEV + 1] & ~KEYSCALE_MASK, fstream);

        // Extra junk on the end

        fputc(0, fstream);
        fputc(0, fstream);                // Base note offset; unused here
        fputc(0, fstream);
}

static void write_instrument(FILE *fstream, 
                             struct opl_operators *instrument,
                             int percussion)
{
        unsigned int flags = 0;

        if (instrument->opl3) {
                flags |= FL_DOUBLE_VOICE;
        }

        if (percussion) {
                flags |= FL_FIXED_PITCH;
        }

        fputc(flags, fstream);

        fputc(0x00, fstream);
        fputc(0x80, fstream);           // finetune
        fputc(0x00, fstream);           // fixed note

        write_sbi_data(fstream, instrument->ops);
        write_sbi_data(fstream, instrument->ops + 11);
}

static void write_instrument_data(FILE *fstream, 
                                  struct opl_operators *instruments)
{
        int i;

        for (i=0; i<NUM_INSTRUMENTS; ++i) {
                write_instrument(fstream, &instruments[i],
                                 i >= NUM_BASIC_INSTRUMENTS);
        }
}

static void write_instrument_names(FILE *fstream, char **names)
{
        int i;
        char buf[32];

        for (i=0; i<NUM_INSTRUMENTS; ++i) {
                memset(buf, 0, sizeof(buf));
                strcpy(buf, names[i]);
                fwrite(buf, 1, sizeof(buf), fstream);
        }
}

static void output_genmidi(char *filename)
{
        FILE *fstream;

        fstream = fopen(filename, "wb");

        if (fstream == NULL) {
                fprintf(stderr, "Failed to open %s\n", filename);
                exit(-1);
        }

        write_header(fstream);

        write_instrument_data(fstream, opl3_instrs);
        write_instrument_names(fstream, genmidi_instr_names);

        fclose(fstream);
}

int main(int argc, char *argv[])
{
        if (argc != 2) {
                printf("Usage: %s <output filename>\n", argv[0]);
                exit(-1);
        }

        output_genmidi(argv[1]);

        return 0;
}

