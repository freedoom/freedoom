/* wav2lmp.c

Copyright (C) 2002 Nicholai Main

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

******************

Processes all .wav in current folder into .lmp
suitable for usage as DOOM DS* sounds.

Assumes little-endian cpu.

should compile on a linux box with gcc with no problems.  i successfully compiled
and ran it using DJGPP (gcc and friends for dos).
will probably compile under most C compilers with no problems; there's nothing
special about the code.

code is a little dirty, but safe; no real potential for damage,
other than the fact that it overwrites without warning any .lmp
files in the current directory.

uses a very strict RIFF interpretation, but i softened it up to the point that it will
convert all current freedoom .wavs and should really be able to convert any .wav

supports 16 bit sounds; it will crunch them to 8 bit (because this is all doom allows).
makes no conversion on samplerate (this is why i wrote it to hopefully be better than
deutex in this respect), the one exception being if the sample rate is greater than
65535, it will not convert that file (because this is all doom allows).  dvd audio is
66150 right?  oh well, no dvd quality audio in doom =).

wave specs from
http://ccrma-www.stanford.edu/CCRMA/Courses/422/projects/WaveFormat/

doom audio specs from Matt Fell's unoffical doom specs

output to stdout is very verbose, i STRONGLY reccomend you redirect it to a file

compete with the teen bitches (e.g. crappy spam) at my email address:
uzi666@juno.com

oblivion

*/

#include <dirent.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int process_file (char *name);

int main (void)
{
  DIR *currentdir;
  struct dirent *entry;

  printf ("wav2lmp Copyright (C) 2002 Nicholai Main\n");
  currentdir = opendir (".");
  if (!currentdir)
  {
    printf ("error opening current directory!\n");
    return 1;
  }
  while ((entry = readdir (currentdir)))
    if (strstr ((*entry).d_name, ".wav"))
      process_file ((*entry).d_name);

  closedir (currentdir);
  printf ("finished processing current directory\n");
  return 0;
}


int process_file (char *name)
{
  FILE *fil;
  FILE *fout;
  long filsize;
  long lbuff;
  char buff[4];
  unsigned short doomnumsamples;
  unsigned short doomsamplerate;
  unsigned short ustemp, ustemp2;
  int sampledepth;
  int numsamples, i;
  char *newname;
  unsigned char ctemp;

  fil = fopen (name, "rb");
  if (fil)
  {
    printf ("Opening %s\n", name);
    fseek (fil, 0, SEEK_END);
    filsize = ftell (fil);
    rewind (fil);
    fread (buff, 1, 4, fil); // ChunkID
    if (strncmp (buff, "RIFF", 4) != 0)
    {
      printf ("  format error: ChunkID\n");
      fclose (fil);
      return 1;
    }
    fread (&lbuff, 4, 1, fil); // ChunkSize
    if (lbuff != filsize - 8)
    {
      printf ("  format error: ChunkSize\n");
      fclose (fil);
      return 1;
    }
    fread (buff, 1, 4, fil); // Format
    if (strncmp (buff, "WAVE", 4) != 0)
    {
      printf ("  format error: Format\n");
      fclose (fil);
      return 1;
    }
    fread (buff, 1, 4, fil); // Subchunk1ID
    if (strncmp (buff, "fmt ", 4) != 0)
    {
      printf ("  format error: Subchunk1ID\n");
      fclose (fil);
      return 1;
    }
    fread (&lbuff, 4, 1, fil); // Subchunk1Size
    if (lbuff == 18)
    {
      printf ("  format warning: Subchunk1 includes ExtraParamSize\n");
      printf ("                  does not follow strict RIFF spec\n");
      printf ("                  ignoring ExtraParamSize\n");
      i = 1;
    }
    else if (lbuff == 16)
      i = 0;
    else
    {
      printf ("  format error: Subchunk1Size\n");
      fclose (fil);
      return 1;
    }
    fread (&lbuff, 2, 1, fil); // AudioFormat
    if (lbuff != 1)
    {
      printf ("  format error: AudioFormat (PCM expected)\n");
      printf ("                may be a valid RIFF file but not understood\n");
      fclose (fil);
      return 1;
    }
    fread (&lbuff, 2, 1, fil); // NumChannels
    if (lbuff != 1)
    {
      printf ("  error: RIFF has more than one channel\n");
      fclose (fil);
      return 1;
    }
    fread (&lbuff, 4, 1, fil); // SampleRate
    if (lbuff > 65535)
    {
      printf ("  error: RIFF sample rate is %i\n", lbuff);
      printf ("         doom audio format only supports up to 65535 samples/sec\n");
      fclose (fil);
      return 1;
    }
    else
      doomsamplerate = (unsigned short) lbuff;
    fread (&lbuff, 4, 1, fil); // ByteRate
    fread (&ustemp, 2, 1, fil); // BlockAlign
    fread (&ustemp2, 2, 1, fil); // BitsPerSample
    if (ustemp2 == 16)
    {
      printf ("  warning: RIFF sample depth is 16\n");
      printf ("           doom audio format only supports up to 8 bits/sample\n");
      printf ("           shrinking to 8 bits/sample\n");
      sampledepth = (int) ustemp2;
    }
    else if (ustemp2 == 8)
      sampledepth = (int) ustemp2;
    else
    {
      printf ("  error: RIFF sample depth is %i\n", ustemp2);
      printf ("         doom audio format only supports up to 8 bits/sample\n");
      printf ("         wav2lmp only understands how to shrink 16 bits/sample\n");
      fclose (fil);
      return 1;
    }
    if (ustemp != sampledepth / 8) // NumChannels * BitsPerSample / 8
    {
      printf ("  format error: BlockAlign\n");
      fclose (fil);
      return 1;
    }
    if (lbuff != doomsamplerate * sampledepth / 8)
    { // SampleRate * NumChannels * BitsPerSample / 8
      printf ("  format error: ByteRate\n");
      fclose (fil);
      return 1;
    }
    // if i = 1 then "fmt " has 2 extra bytes
    if (i == 1)
      fread (&ustemp, 2, 1, fil); // ExtraParamSize??

    // some of the RIFFs have extra chunkage.  this is expected.  skip a non "data" chunk
    // if the file is a maliciously invalid RIFF, the while() loop could fseek() all over
    // the file forever, although there is no other danger.
    // in this case kill the process, read the output so far for the invalid RIFF,
    // and kill the person who sent it.
    // if the file is an inadvertantly invalid RIFF, fseek() will hit an error pretty
    // quickly.
    fread (buff, 1, 4, fil); // Subchunk?ID
    while (strncmp (buff, "data", 4) != 0)
    {
      fread (&lbuff, 4, 1, fil); // should be Subchunk?Size
      printf ("  format warning: SubchunkID is not \"data\"\n");
      printf ("                  skipping %i bytes of unknown Subchunk\n", lbuff);
      if (fseek (fil, lbuff, SEEK_CUR) != 0)
      {
        printf ("  format error: could not find a \"data\" Subchunk\n");
        fclose (fil);
        return 1;
      }
      fread (buff, 1, 4, fil); // next Subchunk?ID
    }

    fread (&lbuff, 4, 1, fil); // Subchunk2Size
    // after running wav2lmp and having it reject a large number of files, i discovered
    // that apparently many sound editors have extra space after the end of the data.
    // some samples have no extra space, some have a byte or two, some have 74 or 75 bytes,
    // and some have 140something bytes.  i think this extra space should be ignored.

    // numsamples = (filsize - 44) * 8 / sampledepth; // 44 byte header - old method
    numsamples = (int) lbuff * 8 / sampledepth;

    if (numsamples > 65535)
    {
      printf ("  warning: RIFF contains %i samples\n", numsamples);
      printf ("           doom audio format only supports up to 65535 samples\n");
      printf ("           truncuating to 65535 samples\n");
      doomnumsamples = 65535;
    }
    else
      doomnumsamples = (unsigned short) numsamples;
    printf ("  preparing to write %i samples at %i samples per second\n",
            doomnumsamples, doomsamplerate);
    i = strlen (name);
    newname = malloc (i + 1);
    if (!newname)
    {
      printf ("  error: failed on malloc() of %i bytes\n", i + 1);
      fclose (fil);
      return 1;
    }
    strcpy (newname, name);
    // change .wav to .lmp
    newname[i-3] = 'l';
    newname[i-2] = 'm';
    newname[i-1] = 'p';
    fout = fopen (newname, "wb");
    // can free newname now
    free (newname);
    if (!fout)
    {
      printf ("  error: couldnt open/create %s for writing\n", newname);
      fclose (fil);
      return 1;
    }
    printf ("  writing doom sound format to %s\n", newname);
    printf ("  if you had the cure for cancer in %s, it's too late now =)\n", newname);
    // doom format is ushort 3, samplerate, numsamples, 0, then data
    ustemp = 3;
    ustemp2 = 0;
    if (fwrite (&ustemp, 2, 1, fout) == -1)
    {
      printf ("  error: couldn't write to %s\n", newname);
      fclose (fil);
      fclose (fout);
      return 1;
    }
    if (fwrite (&doomsamplerate, 2, 1, fout) == -1)
    {
      printf ("  error: couldn't write to %s\n", newname);
      fclose (fil);
      fclose (fout);
      return 1;
    }
    if (fwrite (&doomnumsamples, 2, 1, fout) == -1)
    {
      printf ("  error: couldn't write to %s\n", newname);
      fclose (fil);
      fclose (fout);
      return 1;
    }
    if (fwrite (&ustemp2, 2, 1, fout) == -1)
    {
      printf ("  error: couldn't write to %s\n", newname);
      fclose (fil);
      fclose (fout);
      return 1;
    }
    if (sampledepth == 8)
    {
      for (i = 0; i < doomnumsamples; i++)
      {
        fread (&ctemp, 1, 1, fil);
        if (fwrite (&ctemp, 1, 1, fout) == -1)
        {
          printf ("  error: couldn't write to %s\n", newname);
          fclose (fil);
          fclose (fout);
          return 1;
        }
      }
    }
    else // sampledepth is 16
    {
      for (i = 0; i < doomnumsamples; i++)
      {
        fread (&ustemp, 1, 1, fil);
        ctemp = (char) ((ustemp & 0x7fff) >> 8); // signed to unsigned
        if (!(ustemp & 0x8000)) // positive
          ctemp |= 0x80;
        if (fwrite (&ctemp, 1, 1, fout) == -1)
        {
          printf ("  error: couldn't write to %s\n", newname);
          fclose (fil);
          fclose (fout);
          return 1;
        }
      }
    }
    fclose (fil);
    fclose (fout);
    printf ("  successfully wrote sound file\n");
    return 0;
  }
  // else from if (fil)
  printf ("Couldn't open %s\n", name);
  return 1;
}


