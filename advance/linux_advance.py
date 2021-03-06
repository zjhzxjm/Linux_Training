# -*- coding: utf-8 -*-
"""
Author: xujm@realbio.cn
Ver:1.0

"""

import os
import argparse
import logging
from jinja2 import Environment, PackageLoader

parser = argparse.ArgumentParser(description="Program for Linux advance train")
parser.add_argument('-n', '-number', type=int, dest='number', help='Total number of students, not exceed 40', required=True)
parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', help='Enable debug info')
parser.add_argument('--version', action='version', version='1.0')


class Setting:
    home_dir = '/RealBio_Train/home'
    answer_str = 'APTENODTEMATGNCU'
    html_dir = '/var/www/html'


class Student:
    def __init__(self, stu_num):
        self.num = stu_num

    def check_enroll(self):
        c_enroll = []
        for i in range(1, 41):
            stu_name = 'stu' + '{s:0>3s}'.format(s=str(i))
            file_name = Setting.home_dir + '/' + stu_name + '/answer'
            if i <= self.num and not os.path.exists(file_name):
                c_enroll.append('warning')
                logging.debug("un enroll:\t" + file_name)
            elif i <= self.num and os.path.exists(file_name):
                c_enroll.append('init')
            elif i > self.num and os.path.exists(file_name):
                c_enroll.append('error')
                logging.debug("err enroll:\t" + file_name)
            else:
                c_enroll.append('none')
        return c_enroll


class Answer:
    def __init__(self, stu_num):
        self.num = stu_num

    def check_answer(self):
        num = self.num + 1
        c_answer = {}

        for i in range(1, num):
            stu_name = 'stu' + '{s:0>3s}'.format(s=str(i))
            file_name = Setting.home_dir + '/' + stu_name + '/answer'
            with open(file_name) as f_in:
                stu_answer = f_in.read().split()
                logging.debug("stu_answer:\t" + str(stu_answer))

                if len(stu_answer) > 1:
                    for j in range(0, len(Setting.answer_str)):
                        try:
                            c_answer[j].append('error')
                        except KeyError:
                            c_answer[j] = []
                            c_answer[j].append('error')
                elif len(stu_answer) == 0:
                    for j in range(0, len(Setting.answer_str)):
                        try:
                            c_answer[j].append('none')
                        except KeyError:
                            c_answer[j] = []
                            c_answer[j].append('none')
                elif len(stu_answer) == 1:
                    for j in range(0, len(Setting.answer_str)):
                        try:
                            if stu_answer[0][j].upper() == Setting.answer_str[j]:
                                try:
                                    c_answer[j].append('pass')
                                except KeyError:
                                    c_answer[j] = []
                                    c_answer[j].append('pass')
                            else:
                                try:
                                    c_answer[j].append('error')
                                except KeyError:
                                    c_answer[j] = []
                                    c_answer[j].append('error')
                        except IndexError:
                            try:
                                c_answer[j].append('none')
                            except KeyError:
                                c_answer[j] = []
                                c_answer[j].append('none')

        for i in range(num, 41):
            for j in range(0, len(Setting.answer_str)):
                try:
                    c_answer[j].append('none')
                except KeyError:
                    c_answer[j] = []
                    c_answer[j].append('none')

        return c_answer


if __name__ == '__main__':
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format="[%(asctime)s]%(name)s:%(levelname)s:%(message)s",
            filename='debug.log'
        )

    env = Environment(loader=PackageLoader('html', 'templates'))
    template = env.get_template('template.html')
    advance_student = Student(args.number)
    out = Setting.html_dir + '/index0.html'
    O_html = open(out, 'w')

    if len(list(set(advance_student.check_enroll()))) == 2 and 'warning' not in list(set(advance_student.check_enroll())):
        O_html.write(template.render(number='OK', info=advance_student.check_enroll()))
        advance_answer = Answer(args.number)
        for k, v in advance_answer.check_answer().items():
            out = Setting.html_dir + '/index' + str(k+1) + '.html'
            O_html = open(out, 'w')
            v.count('pass')
            O_html.write(template.render(number=v.count('pass'), info=v))
    else:
        O_html.write(template.render(number='ER', info=advance_student.check_enroll()))