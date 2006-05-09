#!/usr/bin/env ruby

IO.popen("find -type f -name '*.gif' | xargs md5sum |sort") do |proc|
    lastline = ''
    lastsum = ''
    proc.each_line do |s|
        s =~ /^(\w+)/
        sum = $1
        if sum == lastsum
            print lastline
            puts s
            lastline = ''
        else
            lastsum = sum
            lastline = s
        end
    end
end

