import socket
chat_list = [["tsetus","testmsg"],["tsetu1s","testmsg"]]
def sand(msg,nick):
    chat_list.append([nick,msg])
def get_last_msg():
    return chat_list[-1]