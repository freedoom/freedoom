titlepic: fd1title.png fd2title.png fdmtitle.png

m_doom.png: ../m_doom.png
	convert -transparent '#00ffff' ../m_doom.png m_doom.png

m_dm.png: ../m_dm.png
	convert -transparent '#00ffff' ../m_dm.png m_dm.png

t_phase1.png: ../t_phase1.png
	convert -transparent '#00ffff' ../t_phase1.png t_phase1.png

t_phase2.png: ../t_phase2.png
	convert -transparent '#00ffff' ../t_phase2.png t_phase2.png

fd1title.png: titlepic.png m_doom.png t_phase1.png
	./create_caption titlepic.png m_doom.png t_phase1.png $@
	cp $@ ../

fd2title.png: titlepic.png m_doom.png t_phase2.png
	./create_caption titlepic.png m_doom.png t_phase2.png $@
	cp $@ ../

fdmtitle.png: freedm_titlepic.png
	./create_caption $< $@
	cp $@ ../

clean:
	rm -f m_dm.png m_doom.png fd1title.png fd2title.png fdmtitle.png   \
	      ../fd1title.png ../fd2title.png ../fdmtitle.png t_phase1.png \
	      t_phase2.png

.PHONY: clean
