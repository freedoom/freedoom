This is a bootstrap wad. deutex requires an IWAD to build wads. This
wad contains all the lumps deutex needs: PLAYPAL (the freedoom PLAYPAL),
an empty TEXTURE1 lump and a PNAMES lump with one lump in (deutex needs
PNAMES lumps to have at least one entry)

deutex includes all textures from the parent iwad when building wads so
it is important the bootstrap wad has as few textures as possible.



