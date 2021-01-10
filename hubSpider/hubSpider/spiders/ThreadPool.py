#!/usr/bin/env python
# -*- coding:utf-8 -*-
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import queue
import threading
import contextlib
import time


StopEvent = object()


class ThreadPool(object):

    def __init__(self, max_num):
        self.q = queue.Queue()#存放任务的队列
        self.max_num = max_num#最大线程并发数

        self.terminal = False#如果为True 终止所有线程，不再获取新任务
        self.generate_list = [] #已经创建的线程
        self.free_list = []#闲置的线程
        self.run_sum_time=0

    def run(self, func, args, callback=None):
        """
        线程池执行一个任务
        :param func: 任务函数
        :param args: 任务函数所需参数
        :param callback: 任务执行失败或成功后执行的回调函数，回调函数有两个参数1、任务函数执行状态；2、任务函数返回值（默认为None，即：不执行回调函数）
        :return: 如果线程池已经终止，则返回True否则None
        """

        if len(self.free_list) == 0 and len(self.generate_list) < self.max_num: #无空闲线程和不超过最大线程数
            self.generate_thread() # 创建线程
        w = (func, args, callback,)#保存参数为元组
        self.q.put(w)#添加到任务队列
        self.run_sum_time+=1

    def generate_thread(self):
        """
        创建一个线程
        """
        t = threading.Thread(target=self.call)
        t.start()

    def call(self):
        """
        循环去获取任务函数并执行任务函数
        """
        current_thread = threading.currentThread#获取当前线程对象
        self.generate_list.append(current_thread)#添加到已创建线程里

        event = self.q.get() #获取任务
        while event != StopEvent: #如果不为停止信号

            func, arguments, callback = event#分别取值，
            try:
                result = func(*arguments) #运行函数，把结果赋值给result
                status = True   #运行结果是否正常
            except Exception as e:
                status = False #不正常
                result = e  #结果为错误信息
                # print(e)

            if callback is not None: # 是否有回调函数
                try:
                    callback(self.run_sum_time,status, result) #执行回调函数
                except Exception as e:
                    pass

            if self.terminal: # 默认为False ，如果调用terminal方法
                event = StopEvent #停止信号
            else:
                # self.free_list.append(current_thread) #执行完毕任务，添加到闲置列表
                # event = self.q.get()    #获取任务
                # self.free_list.remove(current_thread) #获取到任务之后，从闲置里删除
                with self.worker_state(self.free_list,current_thread):
                    event = self.q.get()


        else:
            self.generate_list.remove(current_thread) #如果收到终止信号，就从已创建的列表删除

    def close(self): #终止线程
        num = len(self.generate_list) #获取总已创建的线程
        while num:
            self.q.put(StopEvent) #添加停止信号，有几个线程就添加几个
            num -= 1

    # 终止线程（清空队列）
    def terminate(self):

        self.terminal = True #更改为True，

        while self.generate_list: #如果有已创建线程存活
            self.q.put(StopEvent) #有几个就发几个信号
        self.q.empty()  #清空队列
    @contextlib.contextmanager
    def worker_state(self,free_list,current_thread):
        free_list.append(current_thread)
        try:
            yield
        finally:
            free_list.remove(current_thread)

