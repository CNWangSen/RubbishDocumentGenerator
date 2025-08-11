from graphviz import Digraph
import os
class Drawer:
	def __init__(self):
		pass
	def FrameDiagramJK(self,path,nodes,marker,rel):
		dot = Digraph(encoding="utf-8", format="png")
		dot.attr("node",fontname="SimHei", rankdir="LR")
		dot.attr("edge",fontname="SimHei", rankdir="LR")
		N=len(nodes)
		for i in range(N):
			dot.node(marker[i],nodes[i], shape='box', style='filled', fillcolor='#f0f0f0')
		edg=[]
		for re in rel:
			edg.append(marker[re[0]]+marker[re[1]])
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
		self.mods=["业务迁移模块",#0
		"双机热备份模块",#1
		"指控端安全加解密模块",#2
		"指控端故障恢复与数据同步模块",#3
		"指控端算法下发算力分配模块",#4
		"指控端自协商快速接入模块",#5
		"资源编排调度模块",#6
		"远程设备管理模块",#7
		"小无人机端边缘设备",#8
		"大无人机端边缘设备",#9
		"大无人艇端边缘设备",#10
		]

		self.draw_InEx([[6,3],[6,4],[6,7],[0,6],[3,1]],True)
		self.draw_InEx([[8,3],[9,3],[10,3],[4,8],[4,9],[4,10],[7,8],[7,9],[7,10],[8,5],[9,5],[10,5]],False)
		
	def draw_InEx(self,SR,isInternal=False):
		marker=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
		for i in range(10):
			marker.append(str(i))
		savepath="pic/jk/external"
		if(isInternal):
			savepath="pic/jk/internal"
		self.D.FrameDiagramJK(savepath,self.mods,marker,SR)
G=Gen()
G.run()