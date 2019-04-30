from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

def setup():
    chatbot = ChatBot('Bot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    trainer='chatterbot.trainers.ListTrainer')
    for file in os.listdir('D:/Code/Chatbot_Project/data/'):
        convData = open(r'D:/Code/Chatbot_Project/data/' + file,encoding='utf-8').readlines()
        chatbot.set_trainer(ListTrainer)
        chatbot.train(convData)
        print("Training completed")
    

setup()
