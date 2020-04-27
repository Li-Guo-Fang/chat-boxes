# socket client end
from socket import *
import time
s = socket(AF_INET, SOCK_STREAM)
remote_host = gethostname()
print ('remote_host:', remote_host)
port = 1200
s.connect((remote_host, port))  
print (u"连接从", s.getsockname()) 
print (u"连接到", s.getpeername())

print (u'从服务器返回消息:')
print (s.recv(1200).decode("utf-8").strip())

while 1:
    username = input("请输入你要使用的英文用户名：\n")
    s.send(('%s\r\n' %username.strip()).encode("utf-8"))
    print (u'从服务器返回消息:')
    response = s.recv(1200).decode("utf-8").strip()
    print (response)	
    if "冲突" not in response:
        break

print("*"*50)
print("""查看当前登录用户列表的命令：list
查看别人给你发送的消息命令要求：getmessage
给别人发送消息,请先输入send，然后按照如下格式发送聊天信息：
username:要发送的消息 
断开连接请输入bye""")
print("*"*50)


while 1:
    send_message=input("请输入发送的信息:\n")   
    if send_message=="getmessage" :

        s.send(('%s:%s\r\n' %(username,send_message)).encode("utf-8"))
        print (u'从服务器返回消息:')
        content = s.recv(1200).decode("utf-8").strip()

        try:
            if "[" in content and ']' in content:
                #服务器返回的是个字符串，我用eval转换为列表对象
                info_list = eval(content)
                for index,info in enumerate(info_list):#遍历
                    #index是序号，info[0]发消息的人名，info[1]是发送的消息体
                    print("%s>用户%s信息：%s" %(index,info[0],info[1]))
            else:
                    print(content)			
        except:
            print("从服务器收到的数据是无效数据！数据为%s" %content)
    elif send_message=="list":
        s.send(('%s\r\n' %send_message).encode("utf-8"))
        print (u'从服务器返回消息:')
        print (s.recv(1200).decode("utf-8").strip())
    elif send_message=="bye":
        s.close()
        break
    elif send_message=="send":
        print("请输入你要给用户发送的消息，消息格式：\n用户名:您要发的消息内容\n")
        info = input(">")
        s.send(('%s:%s\r\n' %(username,info.strip())).encode("utf-8"))#发给server端
        print("发送的消息：",('%s:%s\r\n' %(username,info.strip()))) #打印一下你发送的消息
    else:
        print("输入的消息无效：请使用getmessage、list、bye或者send之一")
        time.sleep(1)
        continue