import pandas as pd
from openai import OpenAI
from translate import Translator
from xpinyin import Pinyin
import os

class Gen:
	def __init__(self):
		self.client = OpenAI(api_key="Your Deepseek API key", base_url="https://api.deepseek.com")
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
		for f in os.listdir("req/modules/"):
			mod = self.readTxt("req/modules/"+f)
			moddesc=mod[0]
			modname = f.split("_")[1].replace(".txt","")
			self.mkdir("text/modules/"+modname+"/")
			for sub_mod_index in range(1,len(mod)):
				submodname=mod[sub_mod_index].replace("\n","")
				print(modname,submodname)
				if(self.override==False and os.path.exists("text/modules/"+modname+"/"+submodname+".txt")):
					continue
				#Content = self.GetPromptFromDS(sysprompt+"这个系统有一个模块名字是"+modname+"，它的功能描述是"+moddesc+"。请给出这个模块的"+submodname+"子模块的技术方案。要结合具体业务场景，最好使用KubeEdge或Kubernetes实现。写成多个自然段，不少于3000字！不要有层级和序号！我只要文字和常规标点符号。不要有多余的回答！我会直接把你的回答填入投标文档的技术方案部分！")
				Content = self.GetPromptFromDS("无人平台分布式协同与控制基础服务平台有一个模块名字是"+modname+"，它的功能描述是"+moddesc+"。请给出这个模块的"+submodname+"子模块的技术方案。写成多个自然段，不少于3000字！只回答汉字、逗号和句号，不要有数字或者引号等其他字符。不要有多余的回答！我会直接把你的回答填入投标文档的技术方案部分！")
				self.writeTxt("text/modules/"+modname+"/"+submodname+".txt",Content)

G=Gen()
G.run()