titlepic: fd1title.gif fd2title.gif fdmtitle.gif

m_doom.gif: ../m_doom.gif
	convert -transparent '#00ffff' ../m_doom.gif m_doom.gif

m_dm.gif: ../m_dm.gif
	convert -transparent '#00ffff' ../m_dm.gif m_dm.gif

t_phase1.gif: ../t_phase1.gif
	convert -transparent '#00ffff' ../t_phase1.gif t_phase1.gif
	
t_phase2.gif: ../t_phase2.gif
	convert -transparent '#00ffff' ../t_phase2.gif t_phase2.gif

fd1title.gif: titlepic.gif m_doom.gif t_phase1.gif
	./create_caption titlepic.gif m_doom.gif t_phase1.gif $@
	cp $@ ../

fd2title.gif: titlepic.gif m_doom.gif t_phase2.gif
	./create_caption titlepic.gif m_doom.gif t_phase2.gif $@
	cp $@ ../

fdmtitle.gif: ../captainw/fdmtitle.gif
	./create_caption ../captainw/fdmtitle.gif $@
	cp $@ ../

clean:
	rm -f m_dm.gif m_doom.gif fd1title.gif fd2title.gif fdmtitle.gif   \
	      ../fd1title.gif ../fd2title.gif ../fdmtitle.gif t_phase1.gif \
	      t_phase2.gif	      

.PHONY: clean
