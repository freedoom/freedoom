# SPDX-License-Identifier: BSD-3-Clause
#
# Configuration file for textgen. This file defines the graphic lumps
# that are generated, and the text to show in each one.
#

import re

# Adjustments for character position based on character pairs. Some
# pairs of characters can fit more snugly together, which looks more
# visually appealing. This is highly dependent on the font graphics,
# and if the font is changed this probably needs to be redone.

FONT_KERNING_RULES = {
    # Right character fits under left character:
    r"T[0ACOSZacos]": -2,
    r"V[OC]": -2,
    r"Y[ASZacs]": -2,
    r"Y[CO0]": -1,
    r"P[Aa]": -3,
    r"P[7]": -2,
    r"P[Z]": -1,
    r"[0O][Aa]": -1,
    r"S[A]": -1,
    r"Sa": -2,
    r"Wa": -1,
    r"p[a]": -1,
    r"s[ao]": -1,
    r"ta": -2,
    r"v[oc]": -1,
    r"y[oacs]": -1,
    # Left character fits under right character:
    r"L[4Q]": -3,
    r"L[O0CTYtcq]": -2,
    r"L[oyVv]": -1,
    r"l[tTY]": -2,
    r"l[y]": -1,
    r"[0O][4TYy]": -2,
    r"[0O][1]": -1,
    r"Q[1TY]": -2,
    r"A[CGTYt]": -2,
    r"A[cgy]": -1,
    r"a[cTYt]": -2,
    r"a[vVy]": -1,
    # Fits into "hole" in left character:
    r"B[0CGOQ]": -2,
    r"B[0cgq]": -2,
    r"C[0CGOQ]": -3,
    r"C[q]": -2,
    r"C[cgo]": -1,
    r"X[0CO]": -3,
    r"X[Qqco]": -2,
    r"8[0CO]": -3,
    r"8[GQcgqo]": -2,
    r"Z[0CO]": -2,
    r"Z[GQocgq]": -1,
    r"I[0COQcoq]": -1,
    r"K[0CO]": -4,
    r"K[GQ]": -3,
    r"K[cgo]": -2,
    r"K[Eq]": -1,
    r"P[0COQcoq]": -1,
    r"R[0COQcoq]": -1,
    # Fits into "hole" in right character:
    r"[O0][2X8]": -3,
    r"[O0][9Kx]": -2,
    r"[O0][Iik]": -1,
    r"Q[28X]": -2,
    r"Q[9Iix]": -1,
    r"q[IXx]": -1,
    # Just because.
    r"[O0][O0]": -1,
}

white_graphics = {
    "wibp1": "P1",
    "wibp2": "P2",
    "wibp3": "P3",
    "wibp4": "P4",
    "wicolon": ":",
    # These files are for the title screens of Phase 1 and Phase 2
    "t_phase1": "PHASE 1",
    "t_phase2": "PHASE 2",
    # Note: level names are also included in this dictionary, with
    # the data added programatically from the DEHACKED lump, see
    # code below.
}

blue_graphics = {
    "m_disopt": "DISPLAY OPTIONS",
    "m_episod": "Choose Episode:",
    "m_optttl": "OPTIONS",
    "m_skill": "Choose Skill Level:",
}

red_graphics = {
    # Title for the HELP/HELP1 screen:
    "helpttl": "Help",
    # Title for CREDIT
    "freettl": "Freedoom",
    "m_ngame": "New Game",
    "m_option": "Options",
    "m_loadg": "Load Game",
    "m_saveg": "Save Game",
    "m_rdthis": "Read This!",
    "m_quitg": "Quit Game",
    "m_newg": "NEW GAME",
    "m_epi1": "Outpost Outbreak",
    "m_epi2": "Military Labs",
    "m_epi3": "Event Horizon",
    "m_epi4": "Double Impact",
    "m_jkill": "Please don't kill me!",
    "m_rough": "Will this hurt?",
    "m_hurt": "Bring on the pain.",
    "m_ultra": "Extreme Carnage.",
    "m_nmare": "MAYHEM!",
    "m_lgttl": "LOAD GAME",
    "m_sgttl": "SAVE GAME",
    "m_endgam": "End Game",
    "m_messg": "Messages:",
    "m_msgoff": "off",
    "m_msgon": "on",
    "m_msens": "Mouse Sensitivity",
    "m_detail": "Graphic Detail:",
    "m_gdhigh": "high",
    "m_gdlow": "low",
    "m_scrnsz": "Screen Size",
    "m_svol": "Sound Volume",
    "m_sfxvol": "Sfx Volume",
    "m_musvol": "Music Volume",
    "m_disp": "Display",
    "wif": "finished",
    "wiostk": "kills",
    "wiosti": "items",
    "wiscrt2": "secret",
    "wiosts": "scrt",
    "wifrgs": "frgs",
    "witime": "Time:",
    "wisucks": "sucks",
    "wimstt": "Total:",
    "wipar": "Par:",
    "wip1": "P1",
    "wip2": "P2",
    "wip3": "P3",
    "wip4": "P4",
    "wiostf": "f.",
    "wimstar": "you",
    "winum0": "0",
    "winum1": "1",
    "winum2": "2",
    "winum3": "3",
    "winum4": "4",
    "winum5": "5",
    "winum6": "6",
    "winum7": "7",
    "winum8": "8",
    "winum9": "9",
    "wipcnt": "%",
    "wiminus": "-",
    "wienter": "ENTERING",
    "m_pause": "pause",
    # Extra graphics used in PrBoom's menus. Generate these as well
    # so that when we play in PrBoom the menus look consistent.
    "prboom": "PrBoom",
    "m_generl": "General",
    "m_setup": "Setup",
    "m_keybnd": "Key Bindings",
    "m_weap": "Weapons",
    "m_stat": "Status Bar/HUD",
    "m_auto": "Automap",
    "m_enem": "Enemies",
    "m_mess": "Messages",
    "m_chat": "Chat Strings",
    "m_horsen": "horizontal",
    "m_versen": "vertical",
    "m_loksen": "mouse look",
    "m_accel": "acceleration",
    # Extra graphics from SMMU/Eternity Engine:
    "m_about": "about",
    "m_chatm": "Chat Strings",
    "m_compat": "Compatibility",
    "m_demos": "demos",
    "m_dmflag": "deathmatch flags",
    "m_etcopt": "eternity options",
    "m_feat": "Features",
    "m_gset": "game settings",
    "m_hud": "heads up display",
    "m_joyset": "joysticks",
    "m_ldsv": "Load/Save",
    "m_menus": "Menu Options",
    "m_mouse": "mouse options",
    "m_player": "player setup",
    "m_serial": "serial connection",
    "m_sound": "sound options",
    "m_status": "status bar",
    "m_tcpip": "tcp/ip connection",
    "m_video": "video options",
    "m_wad": "load wad",
    "m_wadopt": "wad options",
    # This is from SMMU too, and if we follow things to the letter,
    # ought to be all lower-case. However, same lump name is used
    # by other ports (Zandronum) which expect a taller graphic to
    # match the other main menu graphics. Eternity Engine doesn't
    # use it any more, and on SMMU there's enough space for it.
    "m_multi": "Multiplayer",
    # Crispy Doom's Crispness menu:
    "m_crispy": "Crispness",
}


def read_bex_lump(filename):
    """Read the BEX (Dehacked) lump from the given filename.

    Returns:
        Dictionary mapping from name to value.
    """
    result = {}
    with open(filename) as f:
        for line in f:
            # Ignore comments:
            line = line.strip()
            if len(line) == 0 or line[0] in "#;":
                continue
            # Just split on '=' and interpret that as an
            # assignment. This is primitive and doesn't read
            # like a full BEX parser should, but it's good
            # enough for our purposes here.
            assign = line.split("=", 2)
            if len(assign) != 2:
                continue
            result[assign[0].strip()] = assign[1].strip()
    return result


def update_level_name(lumpname, bexdata, bexname):
    """Set the level name for the given graphic from BEX file.

    Args:
      lumpname: Name of output graphic file.
      bexdata: Dictionary of data read from BEX file.
      bexname: Name of entry in BEX file to use.
    """
    if bexname not in bexdata:
        raise Exception(
            "Level name %s not defined in " "DEHACKED lump!" % bexname
        )
    # Strip "MAP01: " or "E1M2: " etc. from start, if present:
    levelname = re.sub("^\w*\d:\s*", "", bexdata[bexname])
    white_graphics[lumpname] = levelname


freedoom_bex = read_bex_lump("../../lumps/p2_deh.lmp")
freedm_bex = read_bex_lump("../../lumps/fdm_deh.lmp")

for e in range(4):
    for m in range(9):
        # HUSTR_E1M1 from BEX => wilv00
        update_level_name(
            "wilv%i%i" % (e, m), freedoom_bex, "HUSTR_E%iM%i" % (e + 1, m + 1)
        )

for m in range(32):
    # HUSTR_1 => cwilv00
    update_level_name("cwilv%02i" % m, freedoom_bex, "HUSTR_%i" % (m + 1))
    # HUSTR_1 => dmwilv00 (from freedm.bex)
    update_level_name("dmwilv%02i" % m, freedm_bex, "HUSTR_%i" % (m + 1))
