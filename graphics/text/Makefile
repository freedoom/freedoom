TEXTGEN_GRAPHICS = \
  m_detail.gif m_disopt.gif m_disp.gif   m_endgam.gif m_epi1.gif   \
  m_epi2.gif   m_epi3.gif   m_epi4.gif   m_episod.gif m_gdhigh.gif \
  m_gdlow.gif  m_hurt.gif   m_jkill.gif  m_lgttl.gif  m_loadg.gif  \
  m_messg.gif  m_msens.gif  m_msgoff.gif m_msgon.gif  m_musvol.gif \
  m_newg.gif   m_ngame.gif  m_nmare.gif  m_option.gif m_optttl.gif \
  m_pause.gif  m_quitg.gif  m_rdthis.gif m_rough.gif  m_saveg.gif  \
  m_scrnsz.gif m_sfxvol.gif m_sgttl.gif  m_skill.gif  m_svol.gif   \
  m_about.gif  m_accel.gif  m_auto.gif   m_chat.gif   m_chatm.gif  \
  m_compat.gif m_demos.gif  m_dmflag.gif m_enem.gif   m_etcopt.gif \
  m_feat.gif   m_generl.gif m_gset.gif   m_horsen.gif m_hud.gif    \
  m_joyset.gif m_keybnd.gif m_ldsv.gif   m_loksen.gif m_menus.gif  \
  m_mess.gif   m_mouse.gif  m_multi.gif  m_player.gif m_serial.gif \
  m_setup.gif  m_sound.gif  m_stat.gif   m_status.gif m_tcpip.gif  \
  m_versen.gif m_video.gif  m_wad.gif    m_wadopt.gif m_weap.gif   \
  prboom.gif   helpttl.gif  freettl.gif                            \
  m_ultra.gif  wibp1.gif    wibp2.gif    wibp3.gif    wibp4.gif    \
  wicolon.gif  wienter.gif  wif.gif      wifrgs.gif   wipcnt.gif   \
  wiminus.gif  wimstar.gif  wimstt.gif   wiostf.gif   wiosti.gif   \
  wiostk.gif   wiosts.gif   wiscrt2.gif  wisucks.gif  witime.gif   \
  wip1.gif     wip2.gif     wip3.gif     wip4.gif     wipar.gif    \
  winum0.gif   winum1.gif   winum2.gif   winum3.gif   winum4.gif   \
  winum5.gif   winum6.gif   winum7.gif   winum8.gif   winum9.gif   \
  cwilv00.gif  cwilv01.gif  cwilv02.gif  cwilv03.gif  cwilv04.gif  \
  cwilv05.gif  cwilv06.gif  cwilv07.gif  cwilv08.gif  cwilv09.gif  \
  cwilv10.gif  cwilv11.gif  cwilv12.gif  cwilv13.gif  cwilv14.gif  \
  cwilv15.gif  cwilv16.gif  cwilv17.gif  cwilv18.gif  cwilv19.gif  \
  cwilv20.gif  cwilv21.gif  cwilv22.gif  cwilv23.gif  cwilv24.gif  \
  cwilv25.gif  cwilv26.gif  cwilv27.gif  cwilv28.gif  cwilv29.gif  \
  cwilv30.gif  cwilv31.gif                                         \
  wilv00.gif   wilv01.gif   wilv02.gif   wilv03.gif   wilv04.gif   \
  wilv05.gif   wilv06.gif   wilv07.gif   wilv08.gif   wilv10.gif   \
  wilv11.gif   wilv12.gif   wilv13.gif   wilv14.gif   wilv15.gif   \
  wilv16.gif   wilv17.gif   wilv18.gif   wilv20.gif   wilv21.gif   \
  wilv22.gif   wilv23.gif   wilv24.gif   wilv25.gif   wilv26.gif   \
  wilv27.gif   wilv28.gif   wilv30.gif   wilv31.gif   wilv32.gif   \
  wilv33.gif   wilv34.gif   wilv35.gif   wilv36.gif   wilv37.gif   \
  wilv38.gif

all: $(TEXTGEN_GRAPHICS) help.gif credit.gif

# textgen creates multiple outputs, which is awkward to express in
# make. Use a witness file (graphics.stamp) as suggested in the
# automake manual: "Handling Tools that Produce Many Outputs"

$(TEXTGEN_GRAPHICS): graphics.stamp
	@if test -f $@; then :; else \
	  rm -f graphics.stamp; \
	  $(MAKE) data.stamp; \
	fi

graphics.stamp: config.py fontchars ../../lumps/fraggle/freedoom.bex
	@rm -f graphics.tmp
	@touch graphics.tmp
	./textgen
	@mv graphics.tmp $@

# Generate transparent image containing text for the HELP screen:
helptext.png: helpttl.gif
	python smtextgen helptext.png 320x200        \
	   150,5   "file:helpttl.gif"                \
	   10,25   "Weapons"                         \
	   80,25   "file:../../sprites/shota0.gif"   \
	   150,25  "file:../../sprites/sgn2a0.gif"   \
	   210,20  "file:../../sprites/mguna0.gif"   \
	   10,40   "file:../../sprites/launa0.gif"   \
	   80,40   "file:../../sprites/plasa0.gif"   \
	   150,40  "file:../../sprites/bfuga0.gif"   \
	   240,40  "file:../../sprites/csawa0.gif"   \
	   10,67   "Ammo"                            \
	   53,67   "file:../../sprites/clipa0.gif"   \
	   68,62   "file:../../sprites/ammoa0.gif"   \
	   110,67  "Shells"                          \
	   160,67  "file:../../sprites/shela0.gif"   \
	   180,62  "file:../../sprites/sboxa0.gif"   \
	   220,67  "Backpack"                        \
	   290,55  "file:../../sprites/bpaka0.gif"   \
	   10,90   "Missiles"                        \
	   76,78   "file:../../sprites/rocka0.gif"   \
	   95,82   "file:../../sprites/broka0.gif"   \
	   170,90  "Energy"                          \
	   220,90  "file:../../sprites/cella0.gif"   \
	   240,81  "file:../../sprites/celpa0.gif"   \
	   10,115  "Health"                          \
	   63,113  "file:../../sprites/bon1a0.gif"   \
	   78,112  "file:../../sprites/stima0.gif"   \
	   96,107  "file:../../sprites/media0.gif"   \
	   128,107 "file:../../sprites/pstra0.gif"   \
	   170,115 "Armor"                           \
	   220,113 "file:../../sprites/bon2a0.gif"   \
	   240,105 "file:../../sprites/arm1b0.gif"   \
	   280,105 "file:../../sprites/arm2b0.gif"   \
	   145,140 "Map"                             \
	   175,130 "file:../../sprites/pmapa0.gif"   \
	   10,140  "Overdrive"                       \
	   84,132  "file:../../sprites/soula0.gif"   \
	   110,132 "file:../../sprites/megaa0.gif"   \
	   10,163  "Night vis."                      \
	   80,160  "file:../../sprites/pvisa0.gif"   \
	   10,182  "Stealth"                         \
	   67,172  "file:../../sprites/pinsa0.gif"   \
	   115,182 "Invuln."                         \
	   170,174 "file:../../sprites/pinva0.gif"   \
	   255,182 "Keys"                            \
	   246,142 "file:../../sprites/rkeya0.gif"   \
	   261,142 "file:../../sprites/ykeya0.gif"   \
	   276,142 "file:../../sprites/bkeya0.gif"   \
	   246,162 "file:../../sprites/rskua0.gif"   \
	   261,162 "file:../../sprites/yskua0.gif"   \
	   276,162 "file:../../sprites/bskua0.gif"   \
	   130,163 "Hazard suit"                     \
	   215,142 "file:../../sprites/suita0.gif"

# Make background transparent so it can be overlayed.
helptext2.png : helptext.png
	convert helptext.png -transparent '#00ffff' helptext2.png

# Background for the help screen is a color shifted version of INTERPIC:
helpbg.png: ../interpic.gif
	convert ../interpic.gif -fill '#5599ff' -tint 100 helpbg.png

# Draw the overlay with text and sprites onto the background to get the
# HELP screen:
help.gif: helpbg.png helptext2.png
	convert helpbg.png                              \
	    -draw 'image over 0,0 0,0 helptext2.png'     \
	    help.gif

credtext.png: freettl.gif credit.txt
	python smtextgen credtext.png 320x200        \
	   120,5  "file:freettl.gif"                \
	   10,30  "include:credit.txt"

credtext2.png: credtext.png
	convert credtext.png -transparent '#00ffff' credtext2.png

credit.gif: helpbg.png credtext2.png
	convert helpbg.png                             \
	    -draw 'image over 0,0 0,0 credtext2.png'   \
	    credit.gif

clean:
	rm -f $(TEXTGEN_GRAPHICS) helpbg.png help.gif \
	    helptext.png helptext2.png graphics.stamp *.pyc \
	    credtext.png credtext2.png credit.gif \
	    dmwilv*.gif
	rm -fr __pycache__
