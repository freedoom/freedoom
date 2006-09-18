#!/usr/bin/ruby
# attic-me.rb: find resources not symlinked to for moving to attic
# (c) 2006 Jon Dowland <jon@alcopop.org>, see "COPYING" file
# vim: set ts=2:
require "find"

class Regexp # mass match with [].include?
	def ==(str); self.match(str); end
end

class AtticMe < File
	@@ignore = [
		/\.$/, /\.svn/, /\.txt$/i, /\.bmp$/i,
		"Makefile", /aoddoom_skeletons/, /\.mid$/,
		/dummy/, "fakedemo.lmp", "misc-lumps",
		"blank.gif", "nomonst.gif", "titlepic",
	]

	def AtticMe.main
		[	"flats",	"graphics",	"levels",
			"musics",	"patches",	"sounds",
			"textures",	"lumps",	"sprites",
		].each do |dir|
			files     = []
			linked_to = []
			Find.find(dir) { |f| 
				Find.prune if @@ignore.include?(basename(f))
				files << expand_path(f) if file?(f) and not symlink?(f)
				linked_to << expand_path(dir+Separator+readlink(f)) if symlink?(f)
			}
			puts (files - linked_to).join("\n")
		end
	end
end
AtticMe.main
