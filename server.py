# encoding="gbk"
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver  # 事件处理器
from twisted.internet import reactor

class Chat(LineReceiver):

    message_dict={}     
    def __init__(self, users):
        self.users = users   
        self.name = None     #当前连接的用户名
        self.state = "GETNAME" #状态位,起了名：状态就是CHAT

    def connectionMade(self):  # 连接开始，且开始做处理
        if self.name is None:
            self.sendLine(u"你叫什么名字?".encode("utf-8"))

    def connectionLost(self, reason): #连接断开的时候做什么处理
        print("断开时的用户名：",self.name)
        if self.name in self.users:
            del self.users[self.name] 
            try:
                if self.name in Chat.message_dict: #把别人给你发的消息，从消息字典中删除掉
                    del Chat.message_dict[self.name]
            except:
                print("删除用户的聊天记录失败")


    def lineReceived(self, line):  	
        if self.state == "GETNAME":  # 根据状态开始选择不同得内容处理
            print("line:",line)
            self.handle_GETNAME(line.decode("utf-8"))
        else:
            self.handle_CHAT(line.decode("utf-8"))

    def handle_GETNAME(self, name): #处理用户起名字的逻辑
        if name in self.users:
            self.sendLine(u"名字冲突了，请做另外起个用户名.\n".encode("utf-8") )  # 每个用户只能有一个聊天通信存在
            return
        self.sendLine(("欢迎, %s!\n"  %name).encode("utf-8")) #给客户端发送一个消息，告诉你欢迎xxx
        self.name = name #用户发来的名字，赋值给self.name变量，连接的客户端的名字
        self.users[name] = self #把self，自己，放到users字典中（存所有用户的连接对象---Chat的实例--self）
        self.state = "CHAT"  #把用户从GETNAME状态改为CHAT状态


    def handle_CHAT(self, message):  # 处理用户聊天的逻辑

            if "getmessage" in message:  
                username = message.split(":")[0]#取到需要取消息的用户名
                print("*"*2,username,Chat.message_dict)

                if (username  not in Chat.message_dict) or  Chat.message_dict[username] == []:
                    self.users[username].sendLine("没有别人给你发送的数据".encode("utf-8"))
                    print(message,"---->","没有别人给你发送的数据","\n")
                    return
                message_list=Chat.message_dict[username]#把消息的列表取出来
                print(message_list)
                if username in self.users:
                    print(username,self.users[username])

                    self.users[username].sendLine(("%s" % message_list).encode("utf-8"))
                    del Chat.message_dict[username]#删除刚才收走的消息
                return

            elif ":" in message:    
                if message.count(":")!=2:
                    self.sendLine("您发送的消息格式不对，请输入send命令后，按照格式‘用户名:消息’来进行聊天信息发送。".encode("utf8"))
                    print("您发送的消息格式不对，请输入send命令后，按照格式‘用户名:消息’来进行聊天信息发送。")
                    return
                from_username = message.split(":")[0]
                to_username =  message.split(":")[1]

                chat_message = message.split(":")[2]
                if to_username not in Chat.message_dict:#判断接受者是否在消息字典中，不在？声明一个空列表作为value
                    Chat.message_dict[to_username] = []
                Chat.message_dict[to_username].append((from_username,chat_message))#向列表中追加这个消息
                print(message, "---->", "增加了用户%s发送的消息:%s" %(to_username,(from_username,chat_message)) , "\n")
                return

            #查看哪些用户处于登录状态
            elif message.strip() =="list":  
                print("list response")
                self.sendLine((str([username for username in self.users]) + "\n").encode("utf-8"))
                print(message, "---->", (str([username for username in self.users]) + "\n"),"\n")
                return
			
            else:
                send_message= ("""请指定用户名，输入send后，按照格式‘用户名:消息’来进行聊天信息发送。
				\n或者输入list查看当前登录用户\n输入getmessage获取其他用户发给你的聊天信息\n""")
                #print (type(send_message))
                self.sendLine(send_message.encode("utf8"))
                print(message, "---->",send_message,"\n")
                return



class ChatFactory(Factory):  #实现的工厂类，必须定义buildProtocol方法，必须返回一个Protocol子类的实例对象
    def __init__(self):
        self.users = {} 

    def buildProtocol(self, addr):
        return Chat(self.users) 

if __name__ == '__main__':
    reactor.listenTCP(1200, ChatFactory()) 
    print ("开始进入监听状态...")
    reactor.run() 