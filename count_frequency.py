#encoding=utf-8
import pdb,sys
# sys.path.append("./jieba-master/")

import re
# import jieba
# import jieba.analyse
import question_words
from question_words import *

# jieba.analyse.set_idf_path('./jieba-master/extra_dict/idf.txt.big')
# jieba.analyse.set_stop_words('./jieba-master/extra_dict/stop_words.txt')

# def is_zn(c):  # define whether a string is Chinese
# 	if u'\u4e00' <= c <= u'\u9fff':
# 		return True
# 	return False

class DataCollect:
	def __init__(self):
		# self.Mfrequency = dict()
		# self.Mtimestamps = dict()
		# self.Mcontent = dict()
		self.Mnames = dict()
		self.member_questions = dict()
		self.date_questions = dict()
	def readfiles(self,inputdir):
		flag = True
		current_member = 0
		current_timestamp = 0
		count = 0
		with open(inputdir) as fin:
			for line in fin:
				line = line.replace('\r\n','')
				Sline = line.split(' ')
				if flag and Sline[0][:5]!='2014-':  # this is title
					continue
				elif flag and Sline[0][:5]=='2014-':  # this is the first author
					flag = False
					timestamp = line[:22]
					current_timestamp = timestamp
					if "(" in Sline[-1]:
						mc = Sline[-1].split('(')  # get member
					else:
						mc = Sline[-1].split('<')
					member = mc[-1][:-1]
					member_name = mc[0]
					current_member = member
					current_date = Sline[0]
					# if current_member not in self.Mnames.keys():
					self.Mnames[current_member] = member_name  # qq --> nicknames

					# if current_member not in self.Mtimestamps.keys():
					# 	self.Mtimestamps[current_member] = []
					# 	self.Mtimestamps[current_member].append(current_timestamp)
					# 	self.Mfrequency[current_member] = 1
					# else:
					# 	self.Mfrequency[current_member] += 1
					# 	self.Mtimestamps[current_member].append(current_timestamp)
				elif Sline[0][:5]=='2014-' and int(Sline[0][5])<2:   # this is the rest authors
					timestamp = line[:22]
					current_timestamp = timestamp
					# count += 1
					if "(" in Sline[-1]:
						mc = Sline[-1].split('(')  # get member
					else:
						mc = Sline[-1].split("<")
					member = mc[-1][:-1]
					member_name = mc[0]
					current_member = member
					current_date = Sline[0]
					# if current_member not in self.Mnames.keys():
					self.Mnames[current_member] = member_name

					# if current_member not in self.Mtimestamps.keys():
					# 	self.Mtimestamps[current_member] = []
					# 	self.Mtimestamps[current_member].append(current_timestamp)
					# 	self.Mfrequency[current_member] = 1
					# else:
					# 	self.Mfrequency[current_member] += 1
					# 	self.Mtimestamps[current_member].append(current_timestamp)

				elif Sline[0][:5]!='2014-':  # this is content
					Sline[0] = Sline[0].replace(' ','')
					if Sline[0]=='':
						continue
					for word in question_words:
						if word in line:
							# sorted by date
							if current_date in self.date_questions.keys():
								self.date_questions[current_date].append(line)
							else:
								self.date_questions[current_date]=[]
								self.date_questions[current_date].append(line)
							# sorted by member
							if current_member in self.member_questions.keys():
								self.member_questions[current_member].append(line)
							else:
								self.member_questions[current_member]=[]
								self.member_questions[current_member].append(line)
							break

					# if current_member not in self.Mcontent.keys():
					# 	self.Mcontent[current_member] = line
					# else:
					# 	self.Mcontent[current_member] += line

	# def cutwords(self):
	# 	sortedFrequency = sorted(self.Mfrequency.iteritems(), key=lambda d:d[1], reverse = True)
	# 	fw = open('pipsay_2','w')
	# 	count = 0
	# 	fullContent = ''
	# 	for member, frequency in sortedFrequency:
	# 		if member == '10000' or member == '1000000' :
	# 			continue
	# 		wfre = dict()
	# 		count += 1
	# 		if count>50:
	# 			break
	# 		# if member=='272152420':
	# 		# 	print "here"
	# 		content = self.Mcontent[member]
	# 		content = content.replace('\t','')
	# 		fullContent += content
	# 		content = jieba.cut(content,cut_all=True)  # cut_all flag
	# 		# content = jieba.analyse.extract_tags(content,20)
	# 		Scontent = list(content)
			
	# 		for word in Scontent:
	# 			if word in jieba.analyse.STOP_WORDS:
	# 				continue
	# 			if len(word) <4:
	# 				continue
	# 			if word not in wfre.keys():
	# 				wfre[word] = 1
	# 			else:
	# 				wfre[word] += 1
	# 		sortedWordFrequency = sorted(wfre.iteritems(), key=lambda d:d[1], reverse = True)
			
	# 		fw1 = open("./members/"+self.Mnames[member]+".txt","w")
	# 		# fw1.write(str(self.Mnames[member])+" said:\n")
	# 		co = 0
	# 		for word, freq in sortedWordFrequency:
	# 			co += 1
	# 			if(co > 100):
	# 				break
	# 			fw1.write(str(freq).ljust(5)+'\t'+word.encode('utf8').ljust(15)+'\n')
	# 			# if co%4==0:
	# 			# 	fw.write('\r')
	# 		# fw.write('\n...............................................................................\n')
	# 		fw1.close()
		
	# 	fullContent = jieba.cut(fullContent,cut_all=True)
	# 	Scontent = list(fullContent)
	# 	wfre = dict()
	# 	for word in Scontent:
	# 		if word in jieba.analyse.STOP_WORDS or (not is_zn(word)) or word[0]=='.':
	# 			continue
	# 		if len(word) <4:
	# 			continue
	# 		if word not in wfre.keys():
	# 			wfre[word] = 1
	# 		else:
	# 			wfre[word] += 1
	# 	sortedWordFrequency = sorted(wfre.iteritems(), key=lambda d:d[1], reverse = True)
	# 	# fw.write('\n..............................................................................\n')
	# 	co = 0
	# 	for word, freq in sortedWordFrequency:
	# 		co += 1
	# 		if(co > 100):
	# 			break
	# 		fw.write(str(freq).ljust(5)+'\t'+word.encode('utf8').ljust(15)+'\n')
	# 		# if co%4==0:
	# 		# 	fw.write('\r')
	# 	# fw.write('\n..............................................................................\n')

	# 	fw.close()
	# 	# print content

	def printResults(self):
		fw = open('QuestionsByMember','w')
		for member in self.member_questions.keys():
			fw.write('--------------------------'+self.Mnames[member]+':\n')
			for question in self.member_questions[member]:
				fw.write(question+'\n')
			fw.write('\n')
		fw.close()

		fw = open('QuestionsByDate','w')
		# sortedDate = sorted(self.date_questions.iteritems(), key=lambda d:d[0], reverse = True)
		for date in sorted(self.date_questions.keys(), reverse = True):
			fw.write('--------------------------'+date+' :\n')
			for question in self.date_questions[date]:
				fw.write(question+'\n')
			fw.write('\n')
		fw.close()
		
		# sortedFrequency = sorted(self.Mfrequency.iteritems(), key=lambda d:d[1], reverse = True)
		# coun = 0
		# topmembers = []
		# for member, frequency in sortedFrequency:
		# 	# print key, dis
		# 	coun += 1
		# 	topmembers.append(member)
		# 	if coun >20:
		# 		break
		# 	fw.write(str(member).ljust(15)+'\t' + self.Mnames[member].ljust(30)+'\t'+str(frequency).ljust(10)+'\n')
		# fw.close()

		# fw = open('member_content_sample','w')
		# kkeys = sorted(self.Mcontent.keys())
		# for member in topmembers:
		# 	fw.write(member+'\t'+self.Mnames[member]+':\n'+self.Mcontent[member]+'\n')		
		# fw.close()

def main():
	global data
	data = DataCollect()
	data.readfiles('chats.txt')
	# data.readfiles('testRecord.txt')
	print "reading files done"
	# data.cutwords()
	data.printResults()

if __name__ == '__main__':
	main()
