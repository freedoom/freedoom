"""A module for manipulating Doom data structures."""

class Patch:
	def __init__(self, n,x,y):
		self.name = n
		self.yoff = x
		self.xoff =y

	def __str__(self):
		return "*\t%8s\t\t%d\t%d" % (self.name,self.xoff,self.yoff)

class Texture:
	def __init__(self,name,width,height):
		self.name = name
		self.width = width
		self.height = height
		self.patches = []
		self.pixbuf = None

	def __str__(self):
		me   = "%8s\t\t%d\t%d\n" % (self.name,int(self.width),int(self.height))
		kids = "\n".join(map(str, self.patches))
		if kids:
			kids += "\n"
		return (me + kids)

