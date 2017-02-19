titlepic: fd1title.gif fd2title.gif fdmtitle.gif

m_doom.gif: ../m_doom.gif
	convert -transparent '#00ffff' ../m_doom.gif m_doom.gif

m_dm.gif: ../m_dm.gif
	convert -transparent '#00ffff' ../m_dm.gif m_dm.gif

fd1title.gif: titlepic.gif m_doom.gif
	./create_caption titlepic.gif m_doom.gif "Phase 1" $@
	cp $@ ../

fd2title.gif: titlepic.gif m_doom.gif
	./create_caption titlepic.gif m_doom.gif "Phase 2" $@
	cp $@ ../

fdmtitle.gif: ../captainw/fdmtitle.gif
	./create_caption ../captainw/fdmtitle.gif $@
	cp $@ ../

clean:
	rm -f m_dm.gif m_doom.gif fd1title.gif fd2title.gif fdmtitle.gif \
	      ../fd1title.gif ../fd2title.gif ../fdmtitle.gif

.PHONY: clean
