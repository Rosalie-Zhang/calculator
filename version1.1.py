#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter
from functools import partial
import datetime
import math
from urllib.request import urlopen 
from bs4 import BeautifulSoup


# In[2]:


#按钮输入调用
def get_input(entry, argu):
    # 从entry窗口展示中获取输入的内容
    input_data = entry.get()
        # 出现连续+，则第二个+为无效输入，不做任何处理
    if (input_data[-1:] == '+') and (argu == '+'):
        return
    # 出现连续+--，则第三个-为无效输入，不做任何处理
    if (input_data[-2:] == '+-') and (argu == '-'):
        return
    # 窗口已经有--后面字符不能为+或-
    if (input_data[-2:] == '--') and (argu in ['-', '+']):
        return
    # 窗口已经有 ** 后面字符不能为 * 或 /
    if (input_data[-2:] == '**') and (argu in ['*', '/']):
        return
    entry.insert("end", argu)


# In[3]:


# 退格(撤销输入)
def backspace(entry):
    input_len = len(entry.get())
    # 删除entry窗口中最后的字符
    entry.delete(input_len - 1)


# In[4]:


# 清空entry内容(清空窗口)
def clear(entry):
    entry.delete(0, "end")


# In[5]:


#计算
def calc(entry):
    #获取输入
    input_data = entry.get()
    if input_data[0]=='输':
        start=input_data.find(':')
        data=input_data[start+1:]

        #计算剩余的人生
        if  input_data[2]=='你':
            birthday=datetime.datetime.strptime(data,"%Y.%m.%d")
            duration=datetime.datetime.today()-birthday
            leftday=26572-duration.days
            decent=round(duration.days/26572*100,2)
            entry.delete(0, "end")
            entry.insert("end","你的人生剩余{}天，你已度过了{}%的人生".format(leftday,decent))
        #DDL倒计时
        elif input_data[2]=='D':
            DDL=datetime.datetime.strptime(data,"%Y.%m.%d")
            if(DDL<datetime.datetime.today()):
                entry.delete(0, "end")
                entry.insert("end", "Calculation error")
            else:
                left=DDL-datetime.datetime.today()
                entry.delete(0, "end")
                entry.insert("end","距离ddl还有{}天".format(left.days))
        #节日计算        
        elif input_data[2]=='节':
            str_list = data.split('.')
            int_list = [int(x) for x in str_list]
            today=datetime.datetime.today()
            festival=datetime.datetime(year=today.year,month=int_list[0],day=int_list[1])
            if (today<festival):
                lastfestival=datetime.datetime(year=today.year-1,month=int_list[0],day=int_list[1])
                dura1=today-lastfestival
                dura2=festival-today
            else:
                nextfestival=datetime.datetime(year=today.year+1,month=int_list[0],day=int_list[1])
                dura1=today-festival
                dura2=nextfestival-today
            entry.delete(0, "end")
            entry.insert("end","距上次节日过了{}天，距下次节日还需{}天".format(dura1.days,dura2.days))   
        #计算n天后的日期
        elif input_data[2]=='天':
            d=int(data)
            d1=datetime.datetime.today()
            dt2 = d1 + datetime.timedelta(days=d)
            entry.delete(0, "end")
            entry.insert("end","{}天后的日期是{}".format(d,dt2.date()))
        #计算某事件发生的天数
        elif input_data[2]=='事':
            past=datetime.datetime.strptime(data,"%Y.%m.%d")
            dura=datetime.datetime.today()-past
            entry.delete(0, "end")
            entry.insert("end","该事件已经发生了{}天".format(dura.days))            
        else: 
            entry.delete(0, "end")
            entry.insert("end", "Calculation error")
    else:
        # 计算前判断输入内容是否为空;首字符不能为*/;*/不能连续出现3次;
        if not input_data:
            return
        clear(entry)
        # 异常捕获，在进行数据运算时如果出现异常进行相应处理
        # noinspection PyBroadException
        try:
            # eval() 函数用来执行一个字符串表达式，并返回表达式的值；并将执行结果转换为字符串
            output_data = str(eval(input_data))
        except Exception:
            # 将提示信息输出到窗口
            entry.insert("end", "Calculation error")
        else:
            # 将计算结果显示在窗口中
            if len(output_data) > 20:
                entry.insert("end", "Value overflow")
            else:
                entry.insert("end", output_data)


# In[6]:


# 转换二进制
def turnbin(entry):
    input_data = bin(eval(entry.get()))
    clear(entry)
    entry.insert("end", input_data)


# In[7]:


# 转换为整数
def turnint(entry):
    input_data = round(eval(entry.get()),0)
    clear(entry)
    entry.insert("end", input_data)


# In[8]:


# 计算平均值和方差
def statistics(entry):
    input_data = entry.get()
    clear(entry)
    data=input_data.split('.')
    summ=0
    num=0
    minus=0
    for i in data:
        summ+=eval(i)
        num+=1
    ave=summ/num
    for i in data:
        minus+=(eval(i)-ave)*(eval(i)-ave)
    var=minus/num
    entry.insert("end","平均值为{}，方差为{}".format(ave,var))


# In[9]:


#计算汇率
def exchange(entry):
    input_data=eval(entry.get())
    r = urlopen("https://www.boc.cn/sourcedb/whpj/")
    c = r.read()
    bs_obj = BeautifulSoup(c,"html")
    t = bs_obj.find_all("table")[1]
    all_tr = t.find_all("tr")
    all_tr.pop(0)
    for r in all_tr:
        all_td = r.find_all("td")
        if all_td[0].text=='美元':
            entry.insert("end","人民币相当于{}美元".format(input_data*eval(all_td[4].text)/100))


# In[10]:


#创建主窗口
root= tkinter.Tk()
#设置窗口标题
root.title('Value Your Time Calculator')
# 窗口大小
root.resizable(0,0)
#设置窗口不同部分的颜色
button_bg = 'LightBlue'
math_sign_bg = 'CornflowerBlue'
cal_output_bg = 'SteelBlue'
button_active_bg = 'MidnightBlue'


# In[11]:


# 创建文本框
entry = tkinter.Entry(root, justify="right", font=7,width=70)
entry.grid(row=1, column=0, columnspan=5, padx=10, pady=10)


# In[12]:


def place_button(text, func, func_params, bg=button_bg, **place_params):
    # 偏函数partial，可以理解为定义了一个模板，后续的按钮在模板基础上进行修改或添加特性
    # activebackground：按钮按下后显示颜place_params色
    my_button = partial(tkinter.Button,bd=0,bg=button_bg,font=('Helvetica','10'),width=15,height=2,activebackground=button_active_bg)
    button = my_button(text=text, bg=bg, command=lambda: func(*func_params))
    button.grid(**place_params)


# In[13]:


# 数值输入类按钮
place_button('1', get_input, (entry, '1'), row=6, column=0,padx=5,pady=5)
place_button('2', get_input, (entry, '2'), row=6, column=1,padx=5,pady=5)
place_button('3', get_input, (entry, '3'), row=6, column=2,padx=5,pady=5)
place_button('4', get_input, (entry, '4'), row=5, column=0,padx=5,pady=5)
place_button('5', get_input, (entry, '5'), row=5, column=1,padx=5,pady=5)
place_button('6', get_input, (entry, '6'), row=5, column=2,padx=5,pady=5)
place_button('7', get_input, (entry, '7'), row=4, column=0,padx=5,pady=5)
place_button('8', get_input, (entry, '8'), row=4, column=1,padx=5,pady=5)
place_button('9', get_input, (entry, '9'), row=4, column=2,padx=5,pady=5)
place_button('0', get_input, (entry, '0'), row=7, column=1,padx=5,pady=5)
place_button('.', get_input, (entry, '.'), row=7, column=2,padx=5,pady=5)


# In[14]:


#功能输入类按钮(背景色、触发功能不同)
place_button('<-', backspace, (entry,), row=2, column=2,padx=5,pady=5)
place_button('C', clear, (entry,), row=2, column=3,padx=5,pady=5)
place_button('=', calc, (entry,), bg=cal_output_bg, row=7, column=3,
                 columnspan=2, sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S,padx=5,pady=5)
place_button('﹢', get_input, (entry, '+'), bg=cal_output_bg, row=6, column=3,padx=5,pady=5)
place_button('﹣', get_input, (entry, '-'), bg=cal_output_bg, row=5, column=3,padx=5,pady=5)
place_button('×', get_input, (entry, '*'), bg=cal_output_bg, row=4, column=3,padx=5,pady=5)
place_button('÷', get_input, (entry, '/'), bg=cal_output_bg, row=3, column=3,padx=5,pady=5)


# In[15]:


#运算类型按钮
place_button('生命的剩余时间', get_input, (entry, '输入你的生日（YYYY.MM.DD）:'), bg=math_sign_bg, row=2, column=4,padx=5,pady=5)
place_button('距离DDL的剩余时间', get_input, (entry, '输入DDL的具体日期（YYYY.MM.DD）:'), bg=math_sign_bg, row=3, column=4,padx=5,pady=5)
place_button('节日', get_input, (entry,'输入节日日期（MM.DD）:'), bg=math_sign_bg, row=4, column=4,padx=5,pady=5)
place_button('n天后的日期', get_input, (entry, '输入天数:'), bg=math_sign_bg, row=5, column=4,padx=5,pady=5)
place_button('事件发生距今时间', get_input, (entry, '输入事件发生日期（YYYY.MM.DD）:'), bg=math_sign_bg, row=6, column=4,padx=5,pady=5)
place_button('二进制', turnbin, (entry,), bg=math_sign_bg,row=3, column=2,padx=5,pady=5)
place_button('取整', turnint, (entry,), bg=math_sign_bg,row=7, column=0,padx=5,pady=5)
place_button('实时美元汇率', exchange, (entry,), bg=math_sign_bg,row=2, column=0,
            columnspan=2, sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S,padx=5,pady=5)
place_button('平均值和方差', statistics, (entry,), bg=math_sign_bg,row=3, column=0,
            columnspan=2, sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S,padx=5,pady=5)


# In[16]:


root.mainloop()

