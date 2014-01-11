titlepic: fd1title.gif fd2title.gif fdmtitle.gif

m_doom.gif: ../m_doom.gif
	convert -transparent '#00ffff' ../m_doom.gif m_doom.gif

m_dm.gif: ../m_dm.gif
	convert -transparent '#00ffff' ../m_dm.gif m_dm.gif

fd1title.gif: titlepic.gif m_doom.gif
	./create_caption m_doom.gif "Phase 1" $@

fd2title.gif: titlepic.gif m_doom.gif
	./create_caption m_doom.gif "Phase 2" $@

fdmtitle.gif: titlepic.gif m_dm.gif
	./create_caption m_dm.gif "Deathmatch" $@

clean:
	rm -f m_dm.gif m_doom.gif fd1title.gif fd2title.gif fdmtitle.gif

.PHONY: clean
