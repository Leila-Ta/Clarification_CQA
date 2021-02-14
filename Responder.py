from collections import defaultdict
import xml.etree.ElementTree as ET
import gzip
import os
from datetime import datetime

path = "/english.stackexchange.com/Analyse"

try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)

Secondary_out = open("./english.stackexchange.com.SecondaryUserAnswered.txt", "w")
Outstatistics = open("./english.stackexchange.com.StatisticsSecondary.txt", "w")

Secondary_out.write("PostId"+'\t'+"Clarifying Question"+'\t'+"AnswertoComment"+'\t'+"UserId(Asker)"+'\t'+"UserAsker"+'\t'+"UserId(Secondaryuser)"+'\t'+"SecondaryUser"+'\t'+"NameofMainUser"+'\t'+"Post"+'\t'+"AcceptedAnswer")
Secondary_out.write('\n')
Outstatistics.write("PostId"+'\t'+"Number Of Clarifying Questions"+'\t'+"Number Of Answered Clarifying Question By Secondary User")
Outstatistics.write('\n')

result = ""
postid = ''
owneruserid = ''
tempowneruserid = ''
tempowneruseridfinal = ''

Dict_Comments = defaultdict(dict)
Dict_Post = defaultdict(dict)
Dict_User = defaultdict(dict)
Dict_clarqasker = defaultdict(dict)
Dict_clarqanswer = defaultdict(dict)
Dict_usedclarqanswer = defaultdict(dict)
Dict_Comments_Score = defaultdict(dict)
Dict_Comments_Time = defaultdict(dict)

Dict_analyznumansclaqSecUser = {}
numclaredit = {}
ClaQ = {}
Dict_PostType={}
Dict_Answer={}
Dict_question = {}
num_acceptedanswer={}
Dict_NumClarQHighScore = {}
Dict_NumClarqShortTime = {}

i = ""
tempusername=""
tempusernamefinal = ""
nameaskerclarq = ""

input = gzip.open("./english.stackexchange.com/Posts.xml.gz", 'r')
treepost = ET.parse(input)
rootpost = treepost.getroot()
f=0
Datetime_Sumup= 0.0
Dict_PairClarqAnswer= defaultdict(dict)

#print(rootpost[0].attrib)
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
    #print(elempost.attrib['Id'])


input = gzip.open("./english.stackexchange.com/Users.xml.gz", 'r')
treeuser = ET.parse(input)
rootuser = treeuser.getroot()

#print(rootuser[0].attrib)
for elemuser in rootuser:
    Dict_User[elemuser.attrib['Id']][elemuser.attrib['DisplayName']] = elemuser.attrib['Reputation']


input = gzip.open("./english.stackexchange.com/Comments.xml.gz", 'r')
tree = ET.parse(input)
root = tree.getroot()

for elem in root:
    if (Dict_PostType[elem.attrib['PostId']]=='1'):
        Dict_Comments_Score[elem.attrib['PostId']][elem.attrib['Text']] = elem.attrib['Score']
        Dict_Comments_Time[elem.attrib['PostId']][elem.attrib['Text']] = elem.attrib['CreationDate']
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
    for z, x in v.items():
        if('?' in z):
            Dict_clarqasker[k][z]=x
            Dict_analyznumansclaqSecUser[k]=0
            Dict_NumClarQHighScore[k] = 0
            Dict_NumClarqShortTime[k] = 0

        if(z):
            if (z[0]=='@'):
                Dict_clarqanswer[k][z]=x

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

        if (ui == owneruserid):
            numclaredit[postid] = numclaredit[postid] - 1
            break
        else:
            if (z[0] == '@'):
                tempusername = z.split()
                tempusernameaskerfinal = (tempusername[0]).replace('@', '')

                if (tempusernameaskerfinal == namemainuser):
                    clarqcount += 1
                    ques = Dict_question[k]
                    ques = ques.split('\n')

                    if (k in num_acceptedanswer.keys()):
                        answ = Dict_Answer[num_acceptedanswer[k]]
                        answ = answ.split('\n')

                    for (keyaskerclarq, valaskerclarq) in Dict_User.items():
                        if (ui == keyaskerclarq):
                            for c, b in valaskerclarq.items():
                                nameaskerclarq = c
                # get the name of the asker clarq

                    for ke, va in Dict_clarqanswer.items():
                        if (ke == k):
                            for zz, xx in va.items():
                                tempusername = zz.split()
                                tempusernamefinal = (tempusername[0]).replace('@',
                                                                          '')  # the name at the begining of line(answer)
                                for (keyanswerclarq, valanswerclarq) in Dict_User.items():
                                    if (xx == keyanswerclarq):
                                        for cc, bb in valanswerclarq.items():
                                            nameanswerclarq = cc

                                if (tempusernamefinal == nameaskerclarq):
                                    if (xx!=owneruserid):
                                        datetime_str = (Dict_Comments_Time[k][z]).replace('T', ' ')
                                        datetime_str2 = (Dict_Comments_Time[k][zz]).replace('T', ' ')
                                        datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
                                        datetime_object2 = datetime.strptime(datetime_str2, '%Y-%m-%d %H:%M:%S.%f')
                                        datatime_difference = datetime_object2 - datetime_object
                                        DTD = datatime_difference.total_seconds()

                                        if (datetime_object2 >= datetime_object):
                                            if zz not in Dict_usedclarqanswer[ke]:
                                                Dict_usedclarqanswer[ke][zz] = xx
                                                Datetime_Sumup = Datetime_Sumup + DTD
                                                ques = Dict_question[k]
                                                ques = ques.split('\n')
                                #We don't want to use an answer twice
                                            Secondary_out.write(k + '\t' + z + '\t' + zz + '\t' + str(x) + '\t' + nameaskerclarq + '\t' + str(xx) + '\t' + nameanswerclarq+'\t'+namemainuser+'\t'+str(ques))

                                            if (k in num_acceptedanswer.keys()):
                                                answ = Dict_Answer[num_acceptedanswer[k]]
                                                answ = answ.split('\n')
                                                Secondary_out.write('\t' + str(answ))
                                            Secondary_out.write('\n')

                                            if k not in Dict_analyznumansclaqSecUser.keys():
                                                Dict_analyznumansclaqSecUser[k] = 1
                                            else:
                                                Dict_analyznumansclaqSecUser[k]+= 1
                                            Dict_PairClarqAnswer[k][z] = zz
                                            f = 1
                                            break

                        if f==1:
                            f=0
                            break

                else:
                    numclaredit[postid] = numclaredit[postid]-1
                    break

            else:
                clarqcount += 1
                ques = Dict_question[k]
                ques = ques.split('\n')

                if (k in num_acceptedanswer.keys()):
                    if (num_acceptedanswer[k] in Dict_Answer.keys()):
                        answ = Dict_Answer[num_acceptedanswer[k]]
                        answ = answ.split('\n')

                for (keyaskerclarq, valaskerclarq) in Dict_User.items():
                    if (ui == keyaskerclarq):
                        for c, b in valaskerclarq.items():
                            nameaskerclarq = c
            # get the name of the asker clarq

                for ke, va in Dict_clarqanswer.items():
                    if (ke == k):
                        for zz, xx in va.items():
                            tempusername = zz.split()
                            tempusernamefinal = (tempusername[0]).replace('@',
                                                                      '')  # the name at the begining of line(answer)

                            for (keyanswerclarq, valanswerclarq) in Dict_User.items():
                                if (xx == keyanswerclarq):
                                    for cc, bb in valanswerclarq.items():
                                        nameanswerclarq = cc

                            if (tempusernamefinal == nameaskerclarq):
                                if (xx != owneruserid):
                                    datetime_str = (Dict_Comments_Time[k][z]).replace('T', ' ')
                                    datetime_str2 = (Dict_Comments_Time[k][zz]).replace('T', ' ')
                                    datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
                                    datetime_object2 = datetime.strptime(datetime_str2, '%Y-%m-%d %H:%M:%S.%f')
                                    datatime_difference = datetime_object2 - datetime_object
                                    DTD = datatime_difference.total_seconds()

                                    if (datetime_object2 >= datetime_object):
                                        if zz not in Dict_usedclarqanswer[ke]:
                                            Dict_usedclarqanswer[ke][zz] = xx
                                            Datetime_Sumup = Datetime_Sumup + DTD
                                            ques = Dict_question[k]
                                            ques = ques.split('\n')
                                    # I don't want to use an answer twice
                                            Secondary_out.write(k + '\t' + z + '\t' + zz + '\t' + str(x) + '\t' + nameaskerclarq + '\t' + str(xx) + '\t' + nameanswerclarq+'\t'+namemainuser+'\t'+ str(ques))

                                            if (k in num_acceptedanswer.keys()):
                                                answ = Dict_Answer[num_acceptedanswer[k]]
                                                answ = answ.split('\n')
                                                Secondary_out.write('\t' + str(answ))
                                            Secondary_out.write('\n')

                                            if k not in Dict_analyznumansclaqSecUser.keys():
                                                Dict_analyznumansclaqSecUser[k] = 1
                                            else:
                                                Dict_analyznumansclaqSecUser[k] += 1
                                            Dict_PairClarqAnswer[k][z] = zz
                                            f = 1
                                            break

                        if f == 1:
                            f = 0
                            break

                        # get the name of the users which call in comment(answer them)
for keymain in Dict_PairClarqAnswer:
    Outstatistics.write(keymain+'\t'+str(numclaredit[keymain])+'\t'+str(Dict_analyznumansclaqSecUser[keymain])+'\t'+str(Dict_NumClarQHighScore[keymain])+'\t'+str(Dict_NumClarqShortTime[keymain]))
    Outstatistics.write('\n')

Outstatistics.close()
Secondary_out.close()
