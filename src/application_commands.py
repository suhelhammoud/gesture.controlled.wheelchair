#!/usr/bin/python

import collections

"""
موديل برمجي يحتوي صفين رئيسيسين مع اجرائياتهما و بهدف توصيف رسائل التحكم بين الكمبيوتر و الاردوينو و بهدف تخفيف اعطاء الاوامر الخاطئة نتيجة الضجيج أو عدم دقة الصورة

class CMD:
صف يستخدم من أجل تعريف مجموعة من الأوامر النصية يتم تبادلها مع دارة الاردوينو عبر وصلة بلوتوث
أيضا يحتوي بعض الاجرائيات التي تمثل هذه الاوامر بصيغة نصية مناسبة للطباعة  

class CommandQueue:
صف يمثل مكدّس له حجم ثابت, من اجل كل امر جديد CMD يتم اضافته إلى المكدس أولا ليأخذ مكان أقدم قيمة تم تخزينها في المكدس 
بعدها يتم حساب أكثر أمر تكرارا في المكدس, اذا كانت قيمة التكرار أكبر من عتبة محددة مسبقا من قبل المستخدم عندها يمكن اعتبار أن هذا الأمر الاكثر تكرارا 
هو الامر اللازم إرساله إلى دارة الاردوينو, ماعدا ذلك لا يتم ارسال شيء
الفكرة من هذا الصف هو أن عملية معالجة تقوم بمعالجة اكثر من 25 صورة في الثانية و بالتالي لدينا أكثر من 25 أمر في الثانية,
اذا كان هنالك ضجيج في الصورة و استنتاج أوامر خاطئة في بعض الصور يمكن تخفيف أثر هذه الاوامر الشاذة باستخدام هذا الصف

"""

class CMD:
    NONE = 'N'
    STOP = 'S'
    FORWARD = 'F'
    RIGHT = 'R'
    LEFT = 'L'
    BACKWARD = 'B'

    @staticmethod
    def st(cmd):
        """
        String representation of commands
        :param cmd: string, examples: 'F', 'R', etc
        :return:  string representation, examples: 'Forward', 'RIGHT', etc
        """
        result = {
            CMD.NONE: "NONE",
            CMD.STOP: "STOP",
            CMD.FORWARD: "FORWARD",
            CMD.BACKWARD: "BACKWARD",
            CMD.LEFT: "LEFT",
            CMD.RIGHT: "RIGHT"
        }
        # return result[cmd]
        return result.get(cmd, "ERROR")


class CommandQueue:
    """
    Command buffer with capacity of "maxLength", accumulate the last commands
    Can decide -at any time- which command was the most common one in the last commands
    Attributes:
        :maxLength: capacity of this buffer
        :threshold: integer, minimum number of occurrences to consider the command
        :default_command: CMD, value to be returned if threshold were not reached
    """

    def __init__(self, maxLength, threshold=2, default_command=CMD.STOP):
        """
        :param maxLength: queue length
        :param threshold: minimum frequency to consider the command valid
        :param default_command: 
        """
        initQueue = [default_command for i in range(0, maxLength)]  # initiate an array with default_command
        self.queue = collections.deque(initQueue, maxlen=maxLength)  # get queue instance
        self.threshold = threshold
        self.default_command = default_command

    def add_and_get(self, command, threshold=2):
        """
        Add current command to the buffer and remove the oldest command from the buffer
        :param CMD, command: command to be added
        :param threshold: minimum occurances to consider the command valid for returning
        :return: CMD, the most common command among commands in buffer if its occurrences passes the threshold
            value, otherwise return the default command
        """
        self.queue.append(command)
        counter = collections.Counter(self.queue)
        [(result_command, freq)] = counter.most_common(1)
        if freq >= threshold:
            return result_command
        else:
            return self.default_command

    def add_and_get_threshold(self, command):
        """
        Same as previous method except that the threshold value is not passed in parameters,
        :param command: CMD, command to be added to the buffer
        :return: most comon command that passes the internal threshold value, otherwise return default command
        """
        return self.add_and_get(command, threshold=self.threshold)
