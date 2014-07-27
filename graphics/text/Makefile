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
  prboom.gif   helpttl.gif                                         \
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

all: $(TEXTGEN_GRAPHICS) help.gif

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
helptext.png:
	python smtextgen helptext.png 320x200 \
	   10,25   "Weapons" \
	   10,67   "Ammo" \
	   110,67  "Shells" \
	   220,67  "Backpack" \
	   10,90   "Missiles" \
	   170,90  "Energy" \
	   10,115  "Health" \
	   170,115 "Armor" \
	   145,140 "Map" \
	   10,140  "Overdrive" \
	   10,163  "Night vis" \
	   10,182  "Invisibility" \
	   135,182 "Invuln" \
	   255,182 "Keys"  \
	   130,163 "Hazard suit"

# Build on helptext.png by adding the title and sprites:
helpoverlay.png : helptext.png helpttl.gif
	convert helptext.png \
	    -draw 'image over 150,5   0,0 "helpttl.gif"' \
	    -draw 'image over 80,25   0,0 "../../sprites/shota0.gif"' \
	    -draw 'image over 150,25  0,0 "../../sprites/sgn2a0.gif"' \
	    -draw 'image over 210,20  0,0 "../../sprites/mguna0.gif"' \
	    -draw 'image over 10,40   0,0 "../../sprites/launa0.gif"' \
	    -draw 'image over 80,40   0,0 "../../sprites/plasa0.gif"' \
	    -draw 'image over 150,40  0,0 "../../sprites/bfuga0.gif"' \
	    -draw 'image over 240,40  0,0 "../../sprites/csawa0.gif"' \
	    -draw 'image over 53,67   0,0 "../../sprites/clipa0.gif"' \
	    -draw 'image over 68,62   0,0 "../../sprites/ammoa0.gif"' \
	    -draw 'image over 160,67  0,0 "../../sprites/shela0.gif"' \
	    -draw 'image over 180,62  0,0 "../../sprites/sboxa0.gif"' \
	    -draw 'image over 76,78   0,0 "../../sprites/rocka0.gif"' \
	    -draw 'image over 95,82   0,0 "../../sprites/broka0.gif"' \
	    -draw 'image over 220,90  0,0 "../../sprites/cella0.gif"' \
	    -draw 'image over 240,81  0,0 "../../sprites/celpa0.gif"' \
	    -draw 'image over 290,55  0,0 "../../sprites/bpaka0.gif"' \
	    -draw 'image over 63,113  0,0 "../../sprites/bon1a0.gif"' \
	    -draw 'image over 78,112  0,0 "../../sprites/stima0.gif"' \
	    -draw 'image over 96,107  0,0 "../../sprites/media0.gif"' \
	    -draw 'image over 128,107 0,0 "../../sprites/pstra0.gif"' \
	    -draw 'image over 220,113 0,0 "../../sprites/bon2a0.gif"' \
	    -draw 'image over 240,105 0,0 "../../sprites/arm1b0.gif"' \
	    -draw 'image over 280,105 0,0 "../../sprites/arm2b0.gif"' \
	    -draw 'image over 175,130 0,0 "../../sprites/pmapa0.gif"' \
	    -draw 'image over 84,132  0,0 "../../sprites/soula0.gif"' \
	    -draw 'image over 110,132 0,0 "../../sprites/megaa0.gif"' \
	    -draw 'image over 80,160  0,0 "../../sprites/pvisa0.gif"' \
	    -draw 'image over 100,172 0,0 "../../sprites/pinsa0.gif"' \
	    -draw 'image over 185,174 0,0 "../../sprites/pinva0.gif"' \
	    -draw 'image over 246,142 0,0 "../../sprites/rkeya0.gif"' \
	    -draw 'image over 261,142 0,0 "../../sprites/ykeya0.gif"' \
	    -draw 'image over 276,142 0,0 "../../sprites/bkeya0.gif"' \
	    -draw 'image over 246,162 0,0 "../../sprites/rskua0.gif"' \
	    -draw 'image over 261,162 0,0 "../../sprites/yskua0.gif"' \
	    -draw 'image over 276,162 0,0 "../../sprites/bskua0.gif"' \
	    -draw 'image over 215,142 0,0 "../../sprites/suita0.gif"' \
	    -transparent '#00ffff' \
	    helpoverlay.png

# Background for the help screen is a color shifted version of INTERPIC:
helpbg.png: ../interpic.gif
	convert ../interpic.gif -fill '#5599ff' -tint 100 helpbg.png

# Draw the overlay with text and sprites onto the background to get the
# HELP screen:
help.gif: helpbg.png helpoverlay.png
	convert helpbg.png                                 \
	    -draw 'image over 0,0 0,0 helpoverlay.png'     \
	    help.gif

clean:
	rm -f $(TEXTGEN_GRAPHICS) helpbg.png help.gif \
	    helpoverlay.png helptext.png graphics.stamp *.pyc
