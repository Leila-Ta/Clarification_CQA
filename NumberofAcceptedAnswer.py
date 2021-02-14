from collections import defaultdict
import xml.etree.ElementTree as ET
import gzip
from datetime import datetime
import os

path = "./english.stackexchange.com/Analyse"

try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)

out = open("./english.stackexchange.com.AcceptedAnswer.txt", "w")

out.write("PostId"+'\t'+"PostScore"+'\t'+"AcceptedAnswer"+'\t'+"AnswerScore"+'\t'''"Number Of Clarifying Questions"+'\t'+"Number Of Answered Clarifying Questions By Main User"+'\t'+"Number Of Answered Clarifying Questions By Secondary User"+'\t'+"Number Of Answered Clarifying Questions without Answer")

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
Dict_usedsecondclarqanswer = defaultdict(dict)

Dict_analyzenumanswerclaq = {}
Dict_analyzenumsecondanswerclaq = {}
Dict_analyzenumwithoutanswerclaq = {}
numclaredit = {}
Dict_PostType={}
Dict_Answer={}
Dict_question = {}
num_acceptedanswer={}
Dict_Answer_Score = {}
Dict_question_Score = {}

fl=0
repe= 0
tme=0


input = gzip.open("./Result/Life-Arts/scifi.stackexchange.com/Posts.xml.gz", 'r')
treepost = ET.parse(input)
rootpost = treepost.getroot()

#print(rootpost[0].attrib)
for elempost in rootpost:
    Dict_PostType[elempost.attrib['Id']]=elempost.attrib['PostTypeId']

    if (elempost.attrib['PostTypeId']=='2'):

        Dict_Answer[elempost.attrib['Id']]=elempost.attrib['Body']
        Dict_Answer_Score[elempost.attrib['Id']]=elempost.attrib['Score']
    else:
        if(elempost.attrib['PostTypeId']=='1'):
            Dict_question[elempost.attrib['Id']] = elempost.attrib['Body']

            if ('AcceptedAnswerId' in elempost.attrib):
                num_acceptedanswer[elempost.attrib['Id']]=elempost.attrib['AcceptedAnswerId']
            Dict_question_Score[elempost.attrib['Id']] = elempost.attrib['Score']

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


input = gzip.open("./Result/Life-Arts/scifi.stackexchange.com/Users.xml.gz", 'r')
treeuser = ET.parse(input)
rootuser = treeuser.getroot()

#print(rootuser[0].attrib)
for elemuser in rootuser:
    Dict_User[elemuser.attrib['Id']][elemuser.attrib['DisplayName']] = elemuser.attrib['Reputation']


input = gzip.open("./Result/Life-Arts/scifi.stackexchange.com/Comments.xml.gz", 'r')
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
            Dict_analyzenumsecondanswerclaq[k]=0
            numclaredit[k]=0
            Dict_analyzenumwithoutanswerclaq[k]=0

        if (z):
            if (z[0]=='@'):
                Dict_clarqanswer[k][z]=ui

for pid, pscore in Dict_question_Score.items():
    print(pid)
    out.write('\n')
    out.write(pid+'\t'+pscore+'\t')

    if pid in num_acceptedanswer.keys():
        if num_acceptedanswer[pid] in Dict_Answer_Score.keys():
            out.write('1'+'\t'+Dict_Answer_Score[num_acceptedanswer[pid]]+'\t')
        else:
            out.write('0' + '\t' + 'Null' + '\t')

    else:
        out.write('0'+'\t'+'Null'+'\t')

    if pid in Dict_clarqasker.keys():
        for z,ui in Dict_clarqasker[pid].items():
            postid = pid
            numclaredit[pid] = len(Dict_clarqasker[pid])

            for (key, value) in Dict_Post[pid].items():
                owneruserid = key
            #get the owneruserid

            for (keymuser, valmuser) in Dict_User.items():
                if (owneruserid == keymuser):
                    for ccc, bb in valmuser.items():
                        namemainuser = ccc
                        break
                    break

            if (z[0] == '@'):
                tempusername = z.split()
                tempusernameaskerfinal = (tempusername[0]).replace('@', '')

                if (tempusernameaskerfinal == namemainuser):
                    for (keyaskerclarq, valaskerclarq) in Dict_User.items():
                        if (ui==keyaskerclarq):
                            for c, b in valaskerclarq.items():
                                nameaskerclarq = c
         #get the name of the asker clarq
                    fl = 0

                    for ke, va in Dict_clarqanswer.items():
                        if (ke == pid):
                            for zz, xx in va.items():
                                tempusername = zz.split()
                                tempusernamefinal = (tempusername[0]).replace('@', '') #the name at the begining of line(answer)

                                for (keyanswerclarq, valanswerclarq) in Dict_User.items():
                                    if (xx == keyanswerclarq):
                                        for cc, bb in valanswerclarq.items():
                                            nameanswerclarq = cc

                                if (tempusernamefinal == nameaskerclarq):
                                    datetime_str = (Dict_Comments_Time[pid][z]).replace('T', ' ')
                                    datetime_str2 = (Dict_Comments_Time[pid][zz]).replace('T', ' ')
                                    datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
                                    datetime_object2 = datetime.strptime(datetime_str2, '%Y-%m-%d %H:%M:%S.%f')
                                    datatime_difference = datetime_object2 - datetime_object

                                    for te, useri in Dict_Comments[pid].items():
                                        if useri == keyaskerclarq:
                                            datetime_str3 = (Dict_Comments_Time[pid][te]).replace('T', ' ')
                                            datetime_object3 = datetime.strptime(datetime_str3, '%Y-%m-%d %H:%M:%S.%f')

                                            if (datetime_object2 > datetime_object3 > datetime_object):
                                                repe = 1
                                                break
                                            else:
                                                continue

                                    if (xx==owneruserid):
                                #I don't want to use an answer twice

                                        if(repe!=1):
                                            if (datetime_object2>=datetime_object):
                                                if z not in Dict_usedclarqanswer[ke]:
                                                    Dict_usedclarqanswer[ke][z] = xx

                                                    if pid not in Dict_analyzenumanswerclaq.keys():
                                                        Dict_analyzenumanswerclaq[pid] = 1
                                                    else:
                                                        Dict_analyzenumanswerclaq[pid]+= 1
                                                    fl=1
                                        repe=0

                                    else:
                                        if (repe != 1):
                                            if (datetime_object2 >= datetime_object):
                                                if z not in Dict_usedsecondclarqanswer[ke]:
                                                    Dict_usedsecondclarqanswer[ke][z] = xx

                                                    if pid not in Dict_analyzenumsecondanswerclaq.keys():
                                                        Dict_analyzenumsecondanswerclaq[pid] = 1
                                                    else:
                                                        Dict_analyzenumsecondanswerclaq[pid] += 1
                                                    fl = 1
                                        repe = 0

                    if (fl != 1):
                        if pid not in Dict_analyzenumwithoutanswerclaq.keys():
                            Dict_analyzenumwithoutanswerclaq[pid] = 1
                        else:
                            Dict_analyzenumwithoutanswerclaq[pid] += 1

                    else:
                        fl = 0

                else:
                    numclaredit[pid] -= 1
                    continue

            else:
                if (ui == owneruserid):
                    numclaredit[pid] -= 1
                    continue
                else:
                    for (keyaskerclarq, valaskerclarq) in Dict_User.items():
                        if (ui == keyaskerclarq):
                            for c, b in valaskerclarq.items():
                                nameaskerclarq = c
                                break
                            break
                    # get the name of the asker clarq
                    fl = 0

                    for ke, va in Dict_clarqanswer.items():
                        if (ke == pid):
                            for zz, xx in va.items():
                                tempusername = zz.split()
                                tempusernamefinal = (tempusername[0]).replace('@',
                                                                              '')  # the name at the begining of line(answer)
                                for (keyanswerclarq, valanswerclarq) in Dict_User.items():
                                    if (xx == keyanswerclarq):
                                        for cc, bb in valanswerclarq.items():
                                            nameanswerclarq = cc

                                if (tempusernamefinal == nameaskerclarq):
                                    datetime_str = (Dict_Comments_Time[pid][z]).replace('T', ' ')
                                    datetime_str2 = (Dict_Comments_Time[pid][zz]).replace('T', ' ')
                                    datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
                                    datetime_object2 = datetime.strptime(datetime_str2, '%Y-%m-%d %H:%M:%S.%f')
                                    datatime_difference = datetime_object2 - datetime_object
                                    for te, useri in Dict_Comments[pid].items():
                                        if useri == keyaskerclarq:
                                            datetime_str3 = (Dict_Comments_Time[pid][te]).replace('T', ' ')
                                            datetime_object3 = datetime.strptime(datetime_str3, '%Y-%m-%d %H:%M:%S.%f')
                                            if (datetime_object2 > datetime_object3 > datetime_object):
                                                repe = 1
                                                break
                                            else:
                                                continue
                                    if (xx == owneruserid):
                                        # I don't want to use an answer twice
                                        if (repe != 1):
                                            if (datetime_object2 >= datetime_object):
                                                if z not in Dict_usedclarqanswer[ke]:
                                                    Dict_usedclarqanswer[ke][z] = xx

                                                    if pid not in Dict_analyzenumanswerclaq.keys():
                                                        Dict_analyzenumanswerclaq[pid] = 1
                                                    else:
                                                        Dict_analyzenumanswerclaq[pid] += 1
                                                    fl = 1
                                        repe = 0

                                    else:
                                        if (repe != 1):
                                            if (datetime_object2 >= datetime_object):
                                                if z not in Dict_usedsecondclarqanswer[ke]:
                                                    Dict_usedsecondclarqanswer[ke][z] = xx

                                                    if pid not in Dict_analyzenumsecondanswerclaq.keys():
                                                        Dict_analyzenumsecondanswerclaq[pid] = 1
                                                    else:
                                                        Dict_analyzenumsecondanswerclaq[pid] += 1
                                                    fl = 1
                                        repe = 0

                    if(fl!=1):
                        if pid not in Dict_analyzenumwithoutanswerclaq.keys():
                            Dict_analyzenumwithoutanswerclaq[pid] = 1
                        else:
                            Dict_analyzenumwithoutanswerclaq[pid] += 1

                    else:
                        fl=0
        out.write(str(numclaredit[pid])+'\t'+str(Dict_analyzenumanswerclaq[pid])+'\t'+str(Dict_analyzenumsecondanswerclaq[pid])+'\t'+str(Dict_analyzenumwithoutanswerclaq[pid]))

    else:
        out.write('0'+'\t'+'0'+'\t'+'0'+'\t'+'0')

out.close()
