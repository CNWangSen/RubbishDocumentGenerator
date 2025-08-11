from graphviz import Digraph
import os
class Drawer:
	def __init__(self):
		pass
	def FrameDiagram(self,path,father,son):
		dot = Digraph(encoding="utf-8", format="png")
		dot.attr("node",fontname="SimHei", rankdir="LR")
		dot.attr("edge",fontname="SimHei", rankdir="LR")
		
		CNT = 0
		edg = []
		dot.node('0', father, shape='box', style='filled', fillcolor='#f0f0f0')
		for s in son:
			CNT+=1
			dot.node(str(CNT), s, shape='box')
			edg.append("0"+str(CNT))
		dot.edges(edg)
		dot.render(path, format='png', cleanup=True, view=False)

class Gen:
	def __init__(self):
		self.D = Drawer()
		self.override=False
	def readTxt(self,path):
		with open(path,"r",encoding="utf-8") as ipt:
			data = ipt.readlines()
		return data
	def run(self):
		sysprompt = self.readTxt("req/system.txt")[0]
		for f in os.listdir("req/modules/"):
			mod = self.readTxt("req/modules/"+f)
			modname = f.split("_")[1].replace(".txt","")
			if(self.override==False and os.path.exists("pic/modules/"+modname+".png")):
				continue
			mods = []
			for sub_mod_index in range(1,len(mod)):
				submodname=mod[sub_mod_index].replace("\n","")
				mods.append(submodname)
			self.D.FrameDiagram("pic/modules/"+modname,modname,mods)

G=Gen()
G.run()