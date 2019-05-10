# -*- coding: utf-8 -*-

from random import choice as randomChoice

global passData
global password

passData = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm',
            'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
passData1=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','J', 'K', 'M',
            'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

passData2 =['!', '@', '#', '$', '%', '^', '&', '*']

passData3=['2', '3', '4', '5', '6', '7', '8', '9']



def genpwd():
    password = []
    number = 2
    count = 0
    while count != number:
        password.append(randomChoice(passData))
        password.append(randomChoice(passData1))
        password.append(randomChoice(passData2))
        password.append(randomChoice(passData3))
        count += 1
    x = 0
    p = ''
    while x != len(password):
        p = p + str(password[x])
        x += 1
        #print(p)
    return p


def getpwd(len):
    password = []
    for i in range(0,int(len)):
        password.append(randomChoice(passData))
        password.append(randomChoice(passData1))
        password.append(randomChoice(passData2))
        password.append(randomChoice(passData3))
    x = 0
    p = ''
    while x != int(len):
        p = p + str(password[x])
        x += 1
    return p

