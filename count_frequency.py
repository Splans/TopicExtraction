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
		self.Mnames = dict()
		self.member_questions = dict()
		self.date_questions = dict()
		self.member_freq_week = dict()  # member --> # questions in latest week
		self.member_questions_week = dict() # member --> questions in latest week

	def readfiles(self,inputdir):
		flag = True
		current_member = 0
		current_timestamp = 0
		ob_date = '2014-09-28'
		with open(inputdir) as fin:
			for line in fin:
				line = line.replace('\r\n','')
				Sline = line.split(' ')
				if flag and Sline[0][:5]!='2014-':  # this is title
					continue
				elif flag and Sline[0][:5]=='2014-':  # this is the first author
					flag = False
					if "(" in Sline[-1]:
						mc = Sline[-1].split('(')  # get member
					else:
						mc = Sline[-1].split('<')
					member = mc[-1][:-1]
					member_name = mc[0]
					current_member = member
					current_date = Sline[0]
					if current_date > ob_date:
						if current_member not in self.member_freq_week.keys():
							self.member_freq_week[current_member]= 1
						else:
							self.member_freq_week[current_member] += 1
					self.Mnames[current_member] = member_name  # qq --> nicknames

				elif Sline[0][:5]=='2014-' and int(Sline[0][5])<2:   # this is the rest authors
					if "(" in Sline[-1]:
						mc = Sline[-1].split('(')  # get member
					else:
						mc = Sline[-1].split("<")
					member = mc[-1][:-1]
					member_name = mc[0]
					current_member = member
					current_date = Sline[0]

					if current_date > ob_date:
						if current_member not in self.member_freq_week.keys():
							self.member_freq_week[current_member]= 1
							self.member_questions_week[current_member] = []
						else:
							self.member_freq_week[current_member] += 1

					self.Mnames[current_member] = member_name

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

							# observerd member content
							if current_date > ob_date:
								self.member_questions_week[current_member].append(line)
								
							break

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
		
		fw = open('ActiveMembers','w')
		fwc = open('Candidates','w')
		fwc.write('This document contains active members whose average freq is larger than 20.\n')
		sortedFrequency = sorted(self.member_freq_week.iteritems(), key=lambda d:d[1], reverse = True)
		for member,freq in sortedFrequency:
			Nquestions=len(self.member_questions_week[member])
			# fwc.write(self.Mnames[member]+' Total:' + str(freq)+' Question:'+str(Nquestions)+' Ratio:'+str(float(Nquestions)/float(freq))+'\n')
			if freq/7 > 20:
				fwc.write(self.Mnames[member]+' ' + str(freq)+' '+str(Nquestions)+' '+str(float(Nquestions)/float(freq))+'\n')
			fw.write('--------------------'+self.Mnames[member]+':\n')
			for question in self.member_questions_week[member]:
				fw.write(question+'\n')
			fw.write('\n')

		fw.close()
		fwc.close()
def main():
	global data
	data = DataCollect()
	data.readfiles('chats.txt')
	print "reading files done"
	data.printResults()

if __name__ == '__main__':
	main()
