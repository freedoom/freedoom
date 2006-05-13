#!/usr/bin/env ruby
#
# Find possibly redundant files for removal

valid_files = {}

# all files in the top level dir

for file in Dir.glob("*")
    valid_files[File.expand_path(file)] = 1
end

# all files in immediate subdirs and the files they link to

for file in Dir.glob("*/*")
    stat = File.lstat(file)
    if stat.symlink?
        valid_files[File.expand_path(file)] = 1
        linked = File.readlink(file)
        linked = File.dirname(file) + "/" + linked
        linked = File.expand_path(linked)
        valid_files[linked] = 1
    end
end

# seek out invalid files and build a list

puts "<ul>"
IO.popen("find | grep -v svn") do |proc|
    proc.each_line do |s|
        s = s.chomp
        s.sub!(/^\.\//, '')

        # ignore text files, non-file
        if s !~ /txt$/i && File.stat(s).file? && !valid_files[File.expand_path(s)]
            puts "<li> <a href='#{s}'>#{s}</a>"
        end
    end
end
puts "</ul>"

