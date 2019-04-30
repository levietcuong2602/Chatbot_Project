from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from datetime import datetime
from pyvi import ViTokenizer, ViPosTagger

import io

def get_response(usrText):
    bot = ChatBot('Bot',
                  storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
        # {
        #     'import_path': 'chatterbot.logic.LowConfidenceAdapter',
        #     'threshold': 0.70,
        #     'default_response': 'I am sorry, but I do not understand.'
        # },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'xin chào',
            'output_text': 'Chào bạn mình là chatbot-khách sạn'
        },
        {
            'import_path': 'logicAdapter.TimeLogicAdapter',
        },
    ],
    trainer='chatterbot.trainers.ListTrainer')
    bot.set_trainer(ListTrainer)

    confidence_threshold = 0.50
    f = io.open("vietnamese-stopwords-dash.txt", mode="r", encoding='utf-8')
    list_stopword = [line.rstrip() for line in f]
    while True:
        if usrText.strip()!= 'Bye':
            test = ViTokenizer.tokenize(usrText)
            filtered_words = " ".join(word.replace("_", " ") for word in test.split(" ") if word not in list_stopword)
            # print(filtered_words)
            result = bot.get_response(filtered_words)                       
            # result = bot.get_response(usrText)
            print("confidence: ", result.confidence)
            if result.confidence > confidence_threshold:
                reply = str(result)
                return(reply)
            else:                    
                reply = str("Xin lỗi, tôi không hiểu!")
                return(reply)

        if usrText.strip() == 'Bye':
            return('Bye')
            break
        

        
