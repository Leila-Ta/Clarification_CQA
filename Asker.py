from collections import defaultdict
import xml.etree.ElementTree as ET
import gzip
from datetime import datetime
import os

path = "/english.stackexchange.com/Analyse"

try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)

out = open("./english.stackexchange.com.ClarqMainUserAnswer.txt", "w")
allclarqmainuser = open("./english.stackexchange.com.AllClarQ.txt", "w")
Outstatistics = open("./english.stackexchange.com.Statistics.txt", "w")
OutBasedTime = open("./english.stackexchange.com.ShortTimeResponse.txt", "w")

Outstatistics.write("PostId"+'\t'+"Number Of Clarifying Questions"+'\t'+"Number Of Answered Clarifying Questions By Main User"+'\t'+"Number Of Answered Clarifying Question With High Score in specific Post"+'\t'+"NumClarqShortTime")
Outstatistics.write('\n')
allclarqmainuser.write("PostId"+'\t'+"ClarQScore"+'\t'+"NumofClarQinPost"+'\t'+"Clarq"+'\t'+"Post"+'\t'+"AcceptedAnswer"+'\t'+"AnswertoComment"+'\t'+"UserIdAsker"+'\t'+"NameofAsker"+'\t'+"MainUserId"+'\t'+"NameofMainUser"+'\t'+"TimeDifference")
out.write("PostId"+'\t'+"Clarifying Question"+'\t'+"AnswertoComment"+'\t'+"UserId(Asker)"+'\t'+"UserAsker"+'\t'+"UserId(MainUser)"+'\t'+"MainUser"+'\t'+"Post"+'\t'+"AcceptedAnswer")
out.write('\n')
OutBasedTime.write("PostId" + '\t' + "Clarifying Question" + '\t' + "AnswertoComment" + '\t' + "Response_Time"+'\t'+"Post"+'\t'+"AcceptedAnswer")
OutBasedTime.write('\n')

result = ""
i = ""
tempusername=""
tempusernamefinal = ""
nameaskerclarq = ""
postid = ''
owneruserid = ''
tempowneruserid = ''
tempowneruseridfinal = ''

Dict_Comments = defaultdict(dict)
Dict_Comments_Score = defaultdict(dict)
Dict_Comments_Time = defaultdict(dict)
Dict_Post = defaultdict(dict)
Dict_User = defaultdict(dict)
Dict_clarqasker = defaultdict(dict)
Dict_clarqanswer = defaultdict(dict)
Dict_usedclarqanswer = defaultdict(dict)
Dict_PairClarqAnswer= defaultdict(dict)
Dict_timedifference = defaultdict(dict)

ClaQ = {}
Dict_analyzenumanswerclaq = {}
numclaredit = {}
Dict_NumClarQHighScore = {}
Dict_NumClarqShortTime = {}
Dict_PostType={}
Dict_Answer={}
Dict_question = {}
num_acceptedanswer={}

Datetime_Sumup= 0.0

fl=0

input = gzip.open("./english.stackexchange.com/Posts.xml.gz", 'r')
treepost = ET.parse(input)
rootpost = treepost.getroot()

for elempost in rootpost:
    Dict_PostType[elempost.attrib['Id']]=elempost.attrib['PostTypeId']
    if (elempost.attrib['PostTypeId']=='2'):

        Dict_Answer[elempost.attrib['Id']]=elempost.attrib['Body']
    else:
        if(elempost.attrib['PostTypeId']=='1'):
            Dict_question[elempost.attrib['Id']] = elempost.attrib['Body']
            if ('AcceptedAnswerId' in elempost.attrib):
                num_acceptedanswer[elempost.attrib['Id']]=elempost.attrib['AcceptedAnswerId']
    if('OwnerUserId' in elempost.attrib):
        Dict_Post[elempost.attrib['Id']][elempost.attrib['OwnerUserId']] = elempost.attrib['Body']
    else:
        if ('OwnerDisplayName' in elempost.attrib):
            tempowneruserid = elempost.attrib['OwnerDisplayName']
            tempowneruseridfinal = tempowneruserid.replace('user', '')
            Dict_Post[elempost.attrib['Id']][tempowneruseridfinal] = elempost.attrib['Body']
        else:
            continue


input = gzip.open("./english.stackexchange.com/Users.xml.gz", 'r')
treeuser = ET.parse(input)
rootuser = treeuser.getroot()

for elemuser in rootuser:
    Dict_User[elemuser.attrib['Id']][elemuser.attrib['DisplayName']] = elemuser.attrib['Reputation']


input = gzip.open("./english.stackexchange.com/Comments.xml.gz", 'r')
tree = ET.parse(input)
root = tree.getroot()

for elem in root:
    if (Dict_PostType[elem.attrib['PostId']]=='1'):
        Dict_Comments_Score[elem.attrib['PostId']][elem.attrib['Text']] = elem.attrib['Score']
        Dict_Comments_Time [elem.attrib['PostId']][elem.attrib['Text']] = elem.attrib['CreationDate']
        if('UserId' in elem.attrib):
            Dict_Comments[elem.attrib['PostId']][elem.attrib['Text']] = elem.attrib['UserId']
        else:
            if ('UserId' in elem.attrib):
                tempowneruserid = elem.attrib['UserDisplayName']
                tempowneruseridfinal = tempowneruserid.replace('user', '')
                Dict_Comments[elem.attrib['PostId']][elem.attrib['Text']] = tempowneruseridfinal
            else:
                continue


for k, v in Dict_Comments.items():
    for z, ui in v.items():
        if('?' in z):
            Dict_clarqasker[k][z]=ui
            Dict_analyzenumanswerclaq[k]=0
            Dict_NumClarQHighScore[k] = 0
            Dict_NumClarqShortTime[k] = 0

        if (z):
            if (z[0]=='@'):
                Dict_clarqanswer[k][z]=ui

for k,v in Dict_clarqasker.items():
    clarqcount = 0
    Final_Score = 0

    for z, ui in v.items():
        Final_Score = Final_Score+int(Dict_Comments_Score[k][z])
        print(k)
        postid = k
        numclaredit[postid] = len(Dict_clarqasker[postid])

        for (key, value) in Dict_Post[postid].items():
            owneruserid = key

            #get the owneruserid
        for (keymuser, valmuser) in Dict_User.items():
            if (owneruserid == keymuser):
                for ccc, bb in valmuser.items():
                    namemainuser = ccc

        if (z[0] == '@'):
            tempusername = z.split()
            tempusernameaskerfinal = (tempusername[0]).replace('@', '')

            if (tempusernameaskerfinal == namemainuser):
                clarqcount += 1
                allclarqmainuser.write('\n')
                ques = Dict_question[k]
                ques = ques.split('\n')
                allclarqmainuser.write(k + '\t' + Dict_Comments_Score[k][z] + '\t' + str(clarqcount) + '\t' + z + '\t'+str(ques))

                if (k in num_acceptedanswer.keys()):
                    answ = Dict_Answer[num_acceptedanswer[k]]
                    answ = answ.split('\n')
                    allclarqmainuser.write('\t' + str(answ)+'\t')

                for (keyaskerclarq, valaskerclarq) in Dict_User.items():
                    if (ui==keyaskerclarq):
                        for c, b in valaskerclarq.items():
                            nameaskerclarq = c

         #get the name of the asker clarq
                for ke, va in Dict_clarqanswer.items():
                    if (ke == k):
                        for zz, xx in va.items():
                            tempusername = zz.split()
                            tempusernamefinal = (tempusername[0]).replace('@', '') #the name at the begining of line(answer)

                            for (keyanswerclarq, valanswerclarq) in Dict_User.items():
                                if (xx == keyanswerclarq):
                                    for cc, bb in valanswerclarq.items():
                                        nameanswerclarq = cc

                            if (tempusernamefinal == nameaskerclarq):
                                if (xx==owneruserid):
                                #We don't want to use an answer twice
                                    datetime_str = (Dict_Comments_Time[k][z]).replace('T', ' ')
                                    datetime_str2 = (Dict_Comments_Time[k][zz]).replace('T', ' ')
                                    datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
                                    datetime_object2 = datetime.strptime(datetime_str2, '%Y-%m-%d %H:%M:%S.%f')
                                    datatime_difference = datetime_object2 - datetime_object
                                    DTD = datatime_difference.total_seconds()

                                    if (datetime_object2>=datetime_object):
                                        if zz not in Dict_usedclarqanswer[ke]:
                                            Dict_usedclarqanswer[ke][zz] = xx
                                            Datetime_Sumup = Datetime_Sumup + DTD
                                            ques = Dict_question[k]
                                            ques = ques.split('\n')
                                            out.write(k + '\t' +z + '\t' + zz + '\t' + str(ui) + '\t' + nameaskerclarq + '\t' + str(xx) + '\t' + nameanswerclarq+'\t'+ str(ques))

                                            if (k in num_acceptedanswer.keys()):
                                                answ = Dict_Answer[num_acceptedanswer[k]]
                                                answ = answ.split('\n')
                                                out.write('\t' + str(answ))
                                            out.write('\n')
                                            Dict_timedifference[k][z]=DTD
                                            allclarqmainuser.write(zz + '\t' + str(ui) + '\t' + nameaskerclarq + '\t' + str(xx) + '\t' + nameanswerclarq+'\t'+str(datatime_difference))

                                            if k not in Dict_analyzenumanswerclaq.keys():
                                                Dict_analyzenumanswerclaq[k] = 1
                                            else:
                                                Dict_analyzenumanswerclaq[k]+= 1
                                            Dict_PairClarqAnswer[k][z] = zz
                                            fl = 1
                                            break

                    if fl==1:
                        fl=0
                        break

            else:
                numclaredit[postid] = numclaredit[postid]-1
                continue

        else:
            if (ui == owneruserid):
                numclaredit[postid] = numclaredit[postid]-1
                continue
            else:
                clarqcount += 1
                allclarqmainuser.write('\n')
                ques = Dict_question[k]
                ques = ques.split('\n')
                allclarqmainuser.write(
                    k + '\t' + Dict_Comments_Score[k][z] + '\t' + str(clarqcount) + '\t' + z + '\t' + str(ques))

                if (k in num_acceptedanswer.keys()):
                    print(num_acceptedanswer[k])

                    if(num_acceptedanswer[k] in Dict_Answer.keys()):
                        answ = Dict_Answer[num_acceptedanswer[k]]
                        answ = answ.split('\n')
                        allclarqmainuser.write('\t' + str(answ) + '\t')

                for (keyaskerclarq, valaskerclarq) in Dict_User.items():
                    if (ui == keyaskerclarq):
                        for c, b in valaskerclarq.items():
                            nameaskerclarq = c

                # get the name of the asker clarq
                for ke, va in Dict_clarqanswer.items():
                    if (ke == k):
                        for zz, xx in va.items():
                            tempusername = zz.split()
                            tempusernamefinal = (tempusername[0]).replace('@', '')  # the name at the begining of line(answer)

                            for (keyanswerclarq, valanswerclarq) in Dict_User.items():
                                if (xx == keyanswerclarq):
                                    for cc, bb in valanswerclarq.items():
                                        nameanswerclarq = cc

                            if (tempusernamefinal == nameaskerclarq):
                                if (xx == owneruserid):
                                    # I don't want to use an answer twice
                                    datetime_str = (Dict_Comments_Time[k][z]).replace('T', ' ')
                                    datetime_str2 = (Dict_Comments_Time[k][zz]).replace('T', ' ')
                                    datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
                                    datetime_object2 = datetime.strptime(datetime_str2, '%Y-%m-%d %H:%M:%S.%f')
                                    datatime_difference = datetime_object2 - datetime_object
                                    DTD = datatime_difference.total_seconds()

                                    if (datetime_object2>=datetime_object):
                                        if zz not in Dict_usedclarqanswer[ke]:
                                            Dict_usedclarqanswer[ke][zz] = xx
                                            Datetime_Sumup = Datetime_Sumup + DTD
                                            ques = Dict_question[k]
                                            ques = ques.split('\n')
                                            out.write(k + '\t' + z + '\t' + zz + '\t' + str(
                                                ui) + '\t' + nameaskerclarq + '\t' + str(
                                                xx) + '\t' + nameanswerclarq + '\t' + str(ques))

                                            if (k in num_acceptedanswer.keys()):
                                                answ = Dict_Answer[num_acceptedanswer[k]]
                                                answ = answ.split('\n')
                                                out.write('\t' + str(answ))
                                            out.write('\n')
                                            Dict_timedifference[k][z]=DTD
                                            allclarqmainuser.write(
                                                zz + '\t' + str(ui) + '\t' + nameaskerclarq + '\t' + str(
                                                    xx) + '\t' + nameanswerclarq + '\t' + str(datatime_difference))

                                            if k not in Dict_analyzenumanswerclaq.keys():
                                                Dict_analyzenumanswerclaq[k] = 1
                                            else:
                                                Dict_analyzenumanswerclaq[k] += 1
                                            Dict_PairClarqAnswer[k][z] = zz
                                            fl = 1
                                            break

                    if fl == 1:
                        fl = 0
                        break

    if(clarqcount!=0):
        Final_Score=Final_Score/clarqcount
        Datetime_Sumup = Datetime_Sumup/clarqcount

        for textpr, TextAnswer in Dict_PairClarqAnswer[k].items():
            if (int(Dict_Comments_Score[k][textpr]))>Final_Score:
                Dict_NumClarQHighScore[k]=Dict_NumClarQHighScore[k]+1

            if (Dict_timedifference[k][textpr])<Datetime_Sumup:
                ques = Dict_question[k]
                ques = ques.split('\n')
                OutBasedTime.write(k+'\t'+textpr+'\t'+Dict_PairClarqAnswer[k][textpr]+'\t'+str(Dict_timedifference[k][textpr])+'\t'+str(ques))

                if (k in num_acceptedanswer.keys()):
                    answ = Dict_Answer[num_acceptedanswer[k]]
                    answ = answ.split('\n')
                    OutBasedTime.write('\t' + str(answ))
                OutBasedTime.write('\n')
                Dict_NumClarqShortTime[k]=Dict_NumClarqShortTime[k]+1

for keymain in Dict_PairClarqAnswer:
    Outstatistics.write(keymain+'\t'+str(numclaredit[keymain])+'\t'+str(Dict_analyzenumanswerclaq[keymain])+'\t'+str(Dict_NumClarQHighScore[keymain])+'\t'+str(Dict_NumClarqShortTime[keymain]))
    Outstatistics.write('\n')
                        # get the name of the users which call in comment(answer them)

out.close()
Outstatistics.close()
OutBasedTime.close()
allclarqmainuser.close()
