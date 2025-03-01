import json
import os
from shutil import copy

from loguru import logger

import conf

week = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
week_type = ['单周', '双周']

subject = {
    '语文': '(255, 151, 135',  # 红
    '数学': '(105, 84, 255',  # 蓝
    '英语': '(236, 135, 255',  # 粉
    '生物': '(68, 200, 94',  # 绿
    '地理': '(80, 214, 200',  # 浅蓝
    '政治': '(255, 110, 110',  # 红
    '历史': '(180, 130, 85',  # 棕
    '物理': '(130, 85, 180',  # 紫
    '化学': '(84, 135, 190',  # 蓝
    '美术': '(0, 186, 255',  # 蓝
    '音乐': '255, 101, 158',  # 红
    '体育': '(255, 151, 135',  # 红
    '信息技术': '(84, 135, 190',  # 蓝
    '电脑': '(84, 135, 190',  # 蓝
    '课程表未加载': '(255, 151, 135',  # 红

    '班会': '(255, 151, 135',  # 红
    '自习': '(115, 255, 150',  # 绿
    '课间': '(135, 255, 191',  # 绿
    '大课间': '(255, 151, 135',  # 红
    '放学': '(84, 255, 101',  # 绿
    '暂无课程': '(84, 255, 101',  # 绿
}

subject_icon = {
    '语文': 'chinese',
    '数学': 'math',
    '英语': 'abc',
    '生物': 'biology',
    '地理': 'geography',
    '政治': 'chinese',
    '历史': 'history',
    '物理': 'physics',
    '化学': 'chemistry',
    '美术': 'art',
    '音乐': 'music',
    '体育': 'pe',
    '信息技术': 'it',
    '电脑': 'it',
    '课程表未加载': 'xmark',

    '班会': 'meeting',
    '自习': 'self_study',
    '课间': 'break',
    '大课间': 'pe',
    '放学': 'after_school',
    '暂无课程': 'break',
}

# 简称
subject_abbreviation = {
    '历史': '史'
}

# 获取当前根目录路径
schedule_dir = os.path.join(os.getcwd(), 'config', 'schedule')

class_activity = ['课程/活动', '课间']
time = ['上午', '下午']
class_kind = [
    '自定义',
    '语文',
    '数学',
    '英语',
    '政治',
    '历史',
    '生物',
    '地理',
    '物理',
    '化学',
    '体育',
    '班会',
    '自习',
    '早读',
    '大课间',
    '美术',
    '音乐',
    '信息技术'
]

default_widgets = [
    'widget-time.ui',
    'widget-countdown.ui',
    'widget-current-activity.ui',
    'widget-next-activity.ui'
]

widget_width = {
    'widget-time.ui': 230,
    'widget-countdown.ui': 200,
    'widget-current-activity.ui': 360,
    'widget-next-activity.ui': 290,
    'widget-countdown-custom.ui': 200,
}

widget_conf = {
    '当前日期': 'widget-time.ui',
    '活动倒计时': 'widget-countdown.ui',
    '当前活动': 'widget-current-activity.ui',
    '下一活动': 'widget-next-activity.ui',
    '自定义倒计时': 'widget-countdown-custom.ui',
}

widget_name = {
    'widget-time.ui': '当前日期',
    'widget-countdown.ui': '活动倒计时',
    'widget-current-activity.ui': '当前活动',
    'widget-next-activity.ui': '下一活动',
    'widget-countdown-custom.ui': '自定义倒计时',
}


def get_subject_abbreviation(key):
    if key in subject_abbreviation:
        return subject_abbreviation[key]
    else:
        return key[:1]


# 学科图标
def get_subject_icon(key):
    if key in subject_icon:
        return f'img/{subject_icon[key]}.svg'
    else:
        return f'img/self_study.svg'


# 学科主题色
def subject_color(key):
    if key in subject:
        return f'{subject[key]}'
    else:
        return '(75, 170, 255'


def get_schedule_config():
    schedule_config = []
    # 遍历目标目录下的所有文件
    for file_name in os.listdir(schedule_dir):
        # 找json
        if file_name.endswith('.json') and file_name != 'backup.json':
            # 将文件路径添加到列表
            schedule_config.append(file_name)
    schedule_config.append('添加新课表')
    return schedule_config


def return_default_schedule_number():
    total = 0
    for file_name in os.listdir(schedule_dir):
        # 找json
        if file_name.startswith('新课表 - '):
            total += 1
    return total


def create_new_profile(filename):
    copy('config/default.json', f'config/schedule/{filename}')


def import_schedule(filepath, filename):  # 导入课表
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            check_data = json.load(file)
    except Exception as e:
        logger.error(f"加载数据时出错: {e}")
        return False
    # 校验课程表
    if check_data is None:
        logger.warning('此文件为空')
        return False
    elif not check_data.get('timeline') and not check_data.get('schedule'):
        logger.warning('此文件不是课程表文件')
        return False
    # 转换为标准格式
    if not check_data.get('schedule_even'):
        logger.warning('此课程表格式不支持单双周')
        check_data['schedule_even'] = {str(i): [] for i in range(0, 6)}

    # 保存文件
    try:
        copy(filepath, f'config/schedule/{filename}')
        conf.save_data_to_json(check_data, filename)
        conf.write_conf('General', 'schedule', filename)
        return True
    except Exception as e:
        logger.error(f"保存数据时出错: {e}")
        return e


def export_schedule(filepath, filename):  # 导出课表
    try:
        copy(f'config/schedule/{filename}', filepath)
        return True
    except Exception as e:
        logger.error(f"导出文件时出错: {e}")
        return e


def get_widget_config():
    try:
        with open(f'config/widget.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            c = data
        return c['widgets']
    except Exception as e:
        print(f'ReadWidgetConfigFAILD: {e}')
        return default_widgets


if __name__ == '__main__':
    print('AL-1S')
