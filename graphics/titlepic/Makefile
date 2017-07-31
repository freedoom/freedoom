titlepic: fd1title.png fd2title.png fdmtitle.png

fd1title.png: titlepic.png ../m_doom.png ../t_phase1.png
	./create_caption titlepic.png ../m_doom.png ../t_phase1.png $@
	cp $@ ../

fd2title.png: titlepic.png ../m_doom.png ../t_phase2.png
	./create_caption titlepic.png ../m_doom.png ../t_phase2.png $@
	cp $@ ../

fdmtitle.png: freedm_titlepic.png
	./create_caption $< $@
	cp $@ ../

clean:
	rm -f fd1title.png fd2title.png fdmtitle.png   \
	      ../fd1title.png ../fd2title.png ../fdmtitle.png 
		  
.PHONY: clean
