import json
import os
import configparser as config
from shutil import copy

from win32com.client import Dispatch
from datetime import datetime
from loguru import logger

import list

path = 'config.ini'
conf = config.ConfigParser()
name = 'Class Widgets'


def check_config():
    conf = config.ConfigParser()
    with open(f'config/default_config.json', 'r', encoding='utf-8') as file:  # 加载默认配置
        default_conf = json.load(file)

    if not os.path.exists('config.ini'):  # 如果配置文件不存在，则copy默认配置文件
        conf.read_dict(default_conf)
        with open(path, 'w', encoding='utf-8') as configfile:
            conf.write(configfile)
        logger.info("配置文件不存在，已创建并写入默认配置。")
    else:
        with open(path, 'r', encoding='utf-8') as configfile:
            conf.read_file(configfile)

        if conf['Other']['version'] != default_conf['Other']['version']:  # 如果配置文件版本不同，则更新配置文件
            logger.info(f"配置文件版本不同，将重新适配")
            try:
                for section, options in default_conf.items():
                    if section not in conf:
                        conf[section] = options
                    else:
                        for key, value in options.items():
                            if key not in conf[section]:
                                conf[section][key] = str(value)
                conf.set('Other', 'version', '1.1.6')
                with open(path, 'w', encoding='utf-8') as configfile:
                    conf.write(configfile)
                logger.info(f"配置文件已更新")
            except Exception as e:
                logger.error(f"配置文件更新失败: {e}")


check_config()


# CONFIG
# 读取config
def read_conf(section='General', key=''):
    data = config.ConfigParser()
    try:
        with open(path, 'r', encoding='utf-8') as configfile:
            data.read_file(configfile)
    except FileNotFoundError:
        return None
    except Exception as e:
        logger.error(f'读取配置文件时出错: {e}')
        return None

    if section in data and key in data[section]:
        return data[section][key]
    else:
        return None


# 写入config
def write_conf(section, key, value):
    data = config.ConfigParser()
    try:
        with open(path, 'r', encoding='utf-8') as configfile:
            data.read_file(configfile)
    except FileNotFoundError:
        pass
    except Exception as e:
        logger.error(f'读取配置文件时出错: {e}')
        return None

    if section not in data:
        data.add_section(section)

    data.set(section, key, value)

    with open(path, 'w', encoding='utf-8') as configfile:
        data.write(configfile)


# JSON
def save_data_to_json(new_data, filename):
    # 初始化 data_dict 为一个空字典
    data_dict = {}

    # 如果文件存在，先读取文件中的现有数据
    if os.path.exists(f'config/schedule/{filename}'):
        try:
            with open(f'config/schedule/{filename}', 'r', encoding='utf-8') as file:
                data_dict = json.load(file)
        except Exception as e:
            logger.error(f"读取现有数据时出错: {e}")

    # 更新 data_dict，添加或覆盖新的数据
    data_dict.update(new_data)

    # 将更新后的数据保存回文件
    try:
        with open(f'config/schedule/{filename}', 'w', encoding='utf-8') as file:
            json.dump(data_dict, file, ensure_ascii=False, indent=4)
        return f"数据已成功保存到 config/schedule/{filename}"
    except Exception as e:
        logger.error(f"保存数据时出错: {e}")


def load_from_json(filename):
    """
    从 JSON 文件中加载数据。
    :param filename: 要加载的文件
    :return: 返回从文件中加载的数据字典
    """
    try:
        with open(f'config/schedule/{filename}', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except Exception as e:
        logger.error(f"加载数据时出错: {e}")
        return None


def is_temp_week():
    if read_conf('Temp', 'set_week') is None or read_conf('Temp', 'set_week') == '':
        return False
    else:
        return read_conf('Temp', 'set_week')


def is_temp_schedule():
    if read_conf('Temp', 'temp_schedule') is None or read_conf('Temp', 'temp_schedule') == '':
        return False
    else:
        return read_conf('Temp', 'temp_schedule')


def add_shortcut_to_startmenu(file='', icon=''):
    try:
        if file == "":
            file_path = os.path.realpath(__file__)
        else:
            file_path = os.path.abspath(file)  # 将相对路径转换为绝对路径

        if icon == "":
            icon_path = file_path  # 如果未指定图标路径，则使用程序路径
        else:
            icon_path = os.path.abspath(icon)  # 将相对路径转换为绝对路径

        # 获取开始菜单文件夹路径
        menu_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs')

        # 快捷方式文件名（使用文件名或自定义名称）
        name = os.path.splitext(os.path.basename(file_path))[0]  # 使用文件名作为快捷方式名称
        shortcut_path = os.path.join(menu_folder, f'{name}.lnk')

        # 创建快捷方式
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = file_path
        shortcut.WorkingDirectory = os.path.dirname(file_path)
        shortcut.IconLocation = icon_path  # 设置图标路径
        shortcut.save()
    except Exception as e:
        logger.error(f"创建开始菜单快捷方式时出错: {e}")


def add_shortcut(file='', icon=''):
    try:
        if file == "":
            file_path = os.path.realpath(__file__)
        else:
            file_path = os.path.abspath(file)

        if icon == "":
            icon_path = file_path
        else:
            icon_path = os.path.abspath(icon)

        # 获取桌面文件夹路径
        desktop_folder = os.path.join(os.environ['USERPROFILE'], 'Desktop')

        # 快捷方式文件名（使用文件名或自定义名称）
        name = os.path.splitext(os.path.basename(file_path))[0]  # 使用文件名作为快捷方式名称
        shortcut_path = os.path.join(desktop_folder, f'{name}.lnk')

        # 创建快捷方式
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = file_path
        shortcut.WorkingDirectory = os.path.dirname(file_path)
        shortcut.IconLocation = icon_path  # 设置图标路径
        shortcut.save()
    except Exception as e:
        logger.error(f"创建桌面快捷方式时出错: {e}")


def add_to_startup(file_path='', icon_path=''):  # 注册到开机启动
    if file_path == "":
        file_path = os.path.realpath(__file__)
    else:
        file_path = os.path.abspath(file_path)  # 将相对路径转换为绝对路径

    if icon_path == "":
        icon_path = file_path  # 如果未指定图标路径，则使用程序路径
    else:
        icon_path = os.path.abspath(icon_path)  # 将相对路径转换为绝对路径

    # 获取启动文件夹路径
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

    # 快捷方式文件名（使用文件名或自定义名称）
    name = os.path.splitext(os.path.basename(file_path))[0]  # 使用文件名作为快捷方式名称
    shortcut_path = os.path.join(startup_folder, f'{name}.lnk')

    # 创建快捷方式
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = file_path
    shortcut.WorkingDirectory = os.path.dirname(file_path)
    shortcut.IconLocation = icon_path  # 设置图标路径
    shortcut.save()


def remove_from_startup():
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    shortcut_path = os.path.join(startup_folder, f'{name}.lnk')
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)


def get_time_offset():  # 获取时差偏移
    time_offset = read_conf('General', 'time_offset')
    if time_offset is None or time_offset == '' or time_offset == '0':
        return 0
    else:
        return int(time_offset)


def get_custom_countdown():  # 获取自定义倒计时
    custom_countdown = read_conf('Date', 'countdown_date')
    if custom_countdown is None or custom_countdown == '':
        return '未设置'
    else:
        custom_countdown = datetime.strptime(custom_countdown, '%Y-%m-%d')
        if custom_countdown < datetime.now():
            return '0 天'
        else:
            cd_text = custom_countdown - datetime.now()
            return f'{cd_text.days} 天'
            # return (
            #     f"{cd_text.days} 天 {cd_text.seconds // 3600} 小时 {cd_text.seconds // 60 % 60} 分"
            # )


def get_week_type():  # 获取单双周
    if read_conf('Date', 'start_date') != '':
        start_date = read_conf('Date', 'start_date')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        today = datetime.now()
        week_num = (today - start_date).days // 7 + 1
        if week_num % 2 == 0:
            return 1  # 双周
        else:
            return 0  # 单周
    else:
        return 0  # 默认单周


def get_is_widget_in(widget='example.ui'):
    widgets_list = list.get_widget_config()
    if widget in widgets_list:
        return True
    else:
        return False


def save_widget_conf_to_json(new_data):
    # 初始化 data_dict 为一个空字典
    data_dict = {}
    if os.path.exists(f'config/widget.json'):
        try:
            with open(f'config/widget.json', 'r', encoding='utf-8') as file:
                data_dict = json.load(file)
        except Exception as e:
            print(f"读取现有数据时出错: {e}")
            return e
    data_dict.update(new_data)
    try:
        with open(f'config/widget.json', 'w', encoding='utf-8') as file:
            json.dump(data_dict, file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"保存数据时出错: {e}")
        return e


# 示例使用
test_data_dict = {
    "timeline": {
        "start_time_m": (0, 0),
        "start_time_a": (0, 0),
        "am0": "40",
        "fm0": "10",
        "am1": "30",
        "fm1": "10",
        "am2": "40",
        "aa0": "40",
        "fa0": "10",
        "aa1": "40",
        "fa1": "10",
        "aa2": "40",
    },
    "schedule": {
        0: ['语文', '数学', '英语', '语文', '数学', '英语'],
        1: ['语文', '数学', '英语', '语文', '数学', '英语'],
        2: ['语文', '数学', '英语', '语文', '数学', '英语'],
        3: ['语文', '数学', '英语', '语文', '数学', '英语'],
        4: ['语文', '数学', '英语', '语文', '数学', '英语']
    }
}


if __name__ == '__main__':
    print('AL_1S')
    print(get_week_type())
    # save_data_to_json(test_data_dict, 'schedule-1.json')
    # loaded_data = load_from_json('schedule-1.json')
    # print(loaded_data)
    # schedule = loaded_data.get('schedule')

    # print(schedule['0'])
    # add_shortcut_to_startmenu('Settings.exe', 'img/favicon.ico')