#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018/11/14 11:44
# @Author  : DonnieZhang

import codecs
import copy
import os
import traceback
from subprocess import call

CUR_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
URLS_FILE = CUR_PATH + 'download.txt'


def download_urls():
    with codecs.open(URLS_FILE, 'r', encoding='utf-8-sig') as old_file:
        lines = old_file.readlines()
        # print(lines)
        cur_lines = copy.deepcopy(lines)

    for line in lines:
        line = line.strip()
        url = 'https://www.khanacademy.org' + line

        # path in front of v
        v_front_path = os.path.dirname(os.path.dirname(line))

        # print("v_front_path: " + v_front_path)

        # last path
        v_behind_path = os.path.basename(os.path.normpath(line))
        # print("v_behind_path: " + v_behind_path)

        # linked path
        linked_path = os.path.join(v_front_path + '/', v_behind_path)
        linked_path = linked_path.strip('/')
        # print("linked_path: " + linked_path)

        working_path = os.path.join(CUR_PATH, linked_path)
        # print("working_path: " + working_path)

        # determine whether the path exist or
        # if exist,pass; otherwise, make dirs
        if not os.path.exists(working_path):
            os.makedirs(working_path)
            print('Created new folder: {}'.format(working_path))
        else:
            print('Existed folder: {}'.format(working_path))

        os.chdir(working_path)
        try:
            cmd = 'youtube-dl {} --all-subs'.format(url)
            call(cmd, shell=True)
        except Exception:
            # print or retrieve detailed exception information
            print(traceback.format_exc())
            print('download fail file:', url)
            # traceback.print_exc()
            with codecs.open('download_fail.txt', 'a+', encoding='utf-8-sig') as f:
                f.writelines(traceback.format_exc() + '\n')
                f.writelines(url + '\n')

        with codecs.open(URLS_FILE, 'w', encoding='utf-8-sig') as new_file:
            cur_lines = cur_lines[1:]
            new_file.writelines(cur_lines)


if __name__ == '__main__':
    download_urls()
    print('Done.')
