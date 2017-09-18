# coding=utf8
import configparser
import xlrd
class ConfigHelper(object):

    @staticmethod
    def write_config(section,key ,value, file_name='conf.ini'):
        conf = configparser.ConfigParser()
        conf.read(file_name, encoding="utf-8")
        if not conf.has_section(section):
            conf.add_section(section)
        conf.set(section, key, value)
        conf.write(open(file_name, "w"))

    @staticmethod
    def read_config(section, key, file_name='conf.ini'):
        conf = configparser.ConfigParser()
        conf.read(file_name,encoding="utf-8")
        if not conf.has_section(section):
            return None
        if not conf.has_option(section,key):
            return None
        return conf.get(section,key)

    @staticmethod
    def read_config(section, key):
        conf = configparser.ConfigParser()
        conf.read('conf.ini', encoding="utf-8")
        if not conf.has_section(section):
            return None
        if not conf.has_option(section,key):
            return None
        return conf.get(section, key)

    @staticmethod
    def get_comments():
        data = xlrd.open_workbook('comments.xlsx')
        table = data.sheets()[0]
        return table.col_values(0)




