## 此脚本从csv文件里读取已发testnet的人的信息，自动发送通知邮件。 Author: MoTao
## 读取的csv文件由TESTNET_APPL_LIST这个值决定
## csv文件的格式: [pub-key, NEO-sent, GAS-sent, contract-addr, email] 
## SMTP自动邮箱发送限制：30封

import csv
import smtplib
from email.message import EmailMessage

TESTNET_APPL_LIST = 'sample.csv'

## Log into my own email service
smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
smtpObj.starttls()
emailAdd = input('Enter your email address: ')
pw = input('Enter your email password: ')
smtpObj.login(emailAdd,pw)
print('Successfully logged in to' + emailAdd)


## currently cannot handle non-ascii chars bc you are using SMTP, use python email plugin instead
def sendTestnetEmail(pubKey, contractAddr,email):
	sender = 'test@neo.org'
	receiver = email

	SUBJECT = 'NEO Testnet Assets Sent'
	TEXT = ("""Hi,

The testnet assets you applied for have been sent to the contract address 
%s

You can transfer them to your own standard address as soon as you have created the contract address in your account, which is built by our pub-key. The minimum number of signatures for the contract address is 1. Reference 'Method of getting TEST GAS and TEST NEO' section for more information: http://docs.neo.org/en-us/network/testnet.html 

Mac/Linux users can also use NEO-Python to retrieve testnet funds: 
https://neo-python.readthedocs.io/en/latest/prompt.html#retrieving-neo-testnet-funds

My pub-key is 037fc87f6db91256fe6d0624feeddc1f4d5a2f698bdc5c453b55d1645134c7143b
Your pub-key is %s

Please make sure that you are using the test net and the blockchain is fully synced.

Try the "rebuild index", if the assets didn't show up.

Here is the invitation for you to join the Neo community in the Discord https://discord.gg/R8v48YA .

====Chinese Ver.====

您好!

您申请的测试网NEO和GAS已发送至合约地址
%s

这是一个由你的公钥和我的公钥创建的一个签名数量为1的多方签名地址,需要你参照官网文档及邮件自行创建. 参考文档http://docs.neo.org/zh-cn/network/testnet.html
Mac和Linux用户也可以使用NEO-Python提取测试资产: 
https://neo-python.readthedocs.io/en/latest/prompt.html#retrieving-neo-testnet-funds (英文页面)

我的公钥是 037fc87f6db91256fe6d0624feeddc1f4d5a2f698bdc5c453b55d1645134c7143b
你的公钥是 %s

请确保你连接的是测试网络并且已同步完毕

当资产无法显示时, 请点击"重建钱包索引"

请于一个月之内从合约地址取出, 过期则回收

Discord社区邀请链接https://discord.gg/R8v48YA 

Regards,
Https://neo.org

""" % (contractAddr,pubKey,contractAddr,pubKey))

	msg = EmailMessage()
	msg.set_content(TEXT)
	msg['Subject'] = SUBJECT
	msg['From'] = sender
	msg['To'] = receiver

	sendMailStatus = smtpObj.send_message(msg)
	if sendMailStatus == {}: 
		print('Successfully sent to ' + receiver)
	else: 
		print ('Error: unable to send to ' + receiver)
	return

## start parsing csv
fileObj = open(TESTNET_APPL_LIST)
readerObj = csv.reader(fileObj)
fileData = list(readerObj)
for row in fileData:
	if len(row[0]) != 66:
		continue #skip row that does not contain the right format(also skips 1st row)
	sendTestnetEmail(row[0],row[3],row[4])
	#sendTestnetEmail(row['targetkey'],row['multisig'],row['email'])
	#TODO: append 'sent' to each row

smtpObj.quit()
print('Reached the end of csv file. \nSMTP Exited.')
