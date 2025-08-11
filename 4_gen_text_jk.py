import pandas as pd
from openai import OpenAI
from translate import Translator
import os
T = Translator(from_lang="ZH", to_lang="EN")

class Gen:
	def __init__(self):
		self.client = OpenAI(api_key="sk-9ced44952b564ef2b185a28a419723d6", base_url="https://api.deepseek.com")
		self.override=False
	def GetPromptFromDS(self,DSprompt):
		response = self.client.chat.completions.create(
			model="deepseek-reasoner",
			messages=[
				{"role": "system", "content": "You are a helpful assistant with web access"},
				{"role": "user", "content": DSprompt},
			],
			stream=False,
			extra_body={
				"web_search": True  # 3. 启用联网搜索参数 
			}
		)
		r = response.choices[0].message.content
		return r
	def readTxt(self,path):
		with open(path,"r",encoding="utf-8") as ipt:
			data = ipt.readlines()
		return data
	def writeTxt(self,path,txt):
		with open(path,"w",encoding="utf-8") as opt:
			opt.write(txt)
	def mkdir(self,path):
		try:
			os.mkdir(path)
		except:
			pass
	def run(self):
		sysprompt = self.readTxt("req/system.txt")[0]
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

		self.run_InEx([[6,3],[6,4],[6,7],[0,6],[3,1]],True)
		self.run_InEx([[8,3],[9,3],[10,3],[4,8],[4,9],[4,10],[7,8],[7,9],[7,10],[8,5],[9,5],[10,5]],False)
		
	def run_InEx(self,SR,isInternal=False):
		savepath="text/jk/external.xlsx"
		if(isInternal):
			savepath="text/jk/internal.xlsx"
		if(self.override==False and os.path.exists(savepath)):
			return
		rec=[]
		send=[]
		para=[]
		func=[]
		for SRpair in SR:
			s=self.mods[SRpair[0]]
			r=self.mods[SRpair[1]]
			rec.append(r)
			send.append(s)
			p=""
			while len(p.split("-"))!=3:
				p=self.GetPromptFromDS("无人平台分布式协同与控制基础服务平台中,"+s+"要向"+r+"发送数据,请用中文列举三个发送的参数,用-分隔，不要回答其他内容！")
				print(s,r,p)
			f=self.GetPromptFromDS("无人平台分布式协同与控制基础服务平台中,"+s+"要向"+r+"发送数据:"+p+",请用一句中文描述这次发送的功能，不要有数据和模块的具体名字！不要回答其他内容！")
			print(s,r,f)
			para.append(p)
			func.append(f)
		data = {
			'接收方': rec,
			'发送方': send,
			'接口参数': para,
			'接口功能': func,
		}

		df = pd.DataFrame(data)
		df.to_excel(savepath)
	def Trans(self,path):
		data = pd.read_excel(path)
		para=data["接口参数"]
		para_eng=[]
		for p in para:
			p_e = ""
			ps = p.split("-")
			for i in range(len(ps)):
				p_e+=T.translate(ps[i])
				if(i!=len(ps)-1):
					p_e+="-"
			para_eng.append(p_e)
		data["接口参数英文"]=para_eng
		df = pd.DataFrame(data)
		df.to_excel(path.replace(".xlsx","")+"_trans.xlsx")

G=Gen()
#G.run()
#G.Trans("text/jk/internal.xlsx")
G.Trans("text/jk/external.xlsx")