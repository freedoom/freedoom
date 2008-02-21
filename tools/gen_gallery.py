#!/usr/bin/python
import os,sys,re

# this sucks

patches = [ x for x in os.listdir('.') if re.match(r'.*\.gif$', x) ]
patches.sort()

print '''<style type="text/css">
	div {
		float: left;
		width: 20%;
	}
</style>
'''
print ''.join(['<div><img src="%s" /><br />%s</div>' % (x,x) for x in patches])
