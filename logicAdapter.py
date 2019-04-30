from chatterbot.logic import LogicAdapter
from datetime import datetime

class TimeLogicAdapter(LogicAdapter):
    def __init__(self, **kwargs):
        super(TimeLogicAdapter, self).__init__(**kwargs)
        from nltk import NaiveBayesClassifier

        self.positive = kwargs.get('positive', [
            'bây giờ là mấy giờ',
            'ê này, mấy giờ rồi',
            'bạn biết mấy giờ rồi không',
            'mấy giờ rồi',
            'mấy h rồi?',
            'mấy h rồi hả',
            'bây h là mấy h'
        ])

        self.negative = kwargs.get('negative', [
            'đến giờ đi ngủ rồi',
            'bây giờ phải làm thế nào',
            'bạn biết cách đăng kí học không',
            'hay đó',
            'mày tên là gì'
        ])

        labeled_data = (
            [(name, 0) for name in self.negative] +
            [(name, 1) for name in self.positive]
        )

        train_set = [
            (self.time_question_features(text), n) for (text, n) in labeled_data
        ]

        self.classifier = NaiveBayesClassifier.train(train_set)

    def time_question_features(self, text):
        """
        Provide an analysis of significant features in the string.
        """
        features = {}

        # A list of all words from the known sentences
        all_words = " ".join(self.positive + self.negative).split()

        # A list of the first word in each of the known sentence
        all_first_words = []
        for sentence in self.positive + self.negative:
            all_first_words.append(
                sentence.split(' ', 1)[0]
            )

        for word in text.split():
            features['first_word({})'.format(word)] = (word in all_first_words)

        for word in text.split():
            features['contains({})'.format(word)] = (word in all_words)

        for letter in 'abcdefghijklmnopqrstuvwxyz':
            features['count({})'.format(letter)] = text.lower().count(letter)
            features['has({})'.format(letter)] = (letter in text.lower())

        return features

    def can_process(self, statement):
        return True

    def process(self, statement):
        from chatterbot.conversation import Statement
        
        now = datetime.now()

        time_features = self.time_question_features(statement.text.lower())
        confidence = self.classifier.classify(time_features)
        cur_hour = int(now.hour)
        if 22 <= cur_hour and cur_hour < 4:
            phase = 'đêm'
        elif 4 <= cur_hour and cur_hour < 10:
            phase = 'sáng'
        elif 10 <= cur_hour and cur_hour < 14:
            phase = 'trưa'
        elif 14 <= cur_hour and cur_hour < 19:
            phase = 'chiều'
        else:
            phase = 'tối'
        response = Statement('Bây giờ là ' + now.strftime('%I:%M') + ' ' + phase)

        response.confidence = confidence
        return response