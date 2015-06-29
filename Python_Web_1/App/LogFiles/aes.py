###### THIS FILE DOES NOT USED FOR THE PROJECT ######

#######################
####### imports #######
#######################
from Crypto.Cipher import AES
from random import choice
import os, string

######################
####### config #######
######################
BLOCK_SIZE = 16
key = os.urandom(BLOCK_SIZE)
cipher = AES.new(key)
EOD = '%EofD%'

# get the number of characters that we need
# def pad(s):
# 	return s+((16-len(s) % 16) * '{')

def genString(length=16, chars=string.printable):
	return ''.join([choice(chars) for i in range(length)])

def encrypt(plainText):
	global cipher
	# cipher = AES.new(key)
	dataLength = len(plainText) + len(EOD)
	if dataLength < 16:
		saltLength = 16 - dataLength
	else:
		saltLength = 16 - dataLength % 16
	ss = ''.join([plainText, EOD, genString(saltLength)])
	return cipher.encrypt(ss)

def decrypt(cipherText):
	global cipher
	# cipher = AES.new(key)
	dec = cipher.decrypt(cipherText).decode('utf-8')
	# l = dec.count('{')
	return dec.split(EOD)[0].decode('utf-8')#dec[:len(dec)-l]

