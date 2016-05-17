# Written by Brendan O'Connor, brenocon@gmail.com, www.anyall.org
#  * Originally written Aug. 2005
#  * Posted to gist.github.com/16173 on Oct. 2008

#   Copyright (c) 2003-2006 Open Source Applications Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import datetime
import logging
import random
import re
import io
import types

# I took this code from a gist at github, and it proved pretty useful.
# However I have added some code to actually put the logs into a file and directory in the path specified at the settings.py
# 
# Enjoy, Hamza Ouaghad
# Great gratitude to Mr.Ben Gelb


"""This file has been *heavily* modified to remove the use of global variables, implement
a logging class instead of relying on sys.stdout, remove the function log decorator, remove
the module log decorator, allow color changing on any log call,
allow indentation level changing on any log call, and PEP-8 formatting.

Copyright (C) 2013 Ben Gelb
"""

from newsline.helpers.colors_class import ColorsClass

def formattime(nodel=False, sec=False):
    now  = datetime.datetime.now()
    time = None

    if nodel == True:
        if sec:
            time = "%d%d%d" % (now.hour, now.minute, now.second)
        else:
            time = "%d%d" % (now.hour, now.minute)
    elif nodel == False:
        if sec:
            time = "[%d:%d:%d]" % (now.hour, now.minute, now.second)
        else:
            time = "[%d:%d]" % (now.hour, now.minute)
    elif isinstance(nodel, str):
        if sec:
            time = "[%d%s%d%s%d]" % (now.hour, nodel, now.minute, nodel, now.second)
        else:
            time = "[%d%s%d]" % (now.hour, nodel, now.minute)

    return time

def formatdate(nodel=False):
    now  = datetime.datetime.now()
    date = None

    if nodel == True:
        date = "%i%i%i" % (now.month, now.day, now.year)
    elif nodel == False:
        date = "[%i/%i/%i]" % (now.month, now.day, now.year)
    elif isinstance(nodel, str):
        date = "[%i%s%i%s%i]" % (now.month, nodel, now.day, nodel, now.year)

    return date

class LogBuffer:
    """
    This class serves a string buffer
    """

    @property
    def prefix(self):
        return "%s %s : " % (formatdate("-"), formattime("-", sec=True))

    def __init__(self):
        self._stringio = io.StringIO()

    def __str__(self):
        return self._stringio.getvalue()

    def __push(self, *objects, sep=' ', end=''):
        print(*objects, sep=sep, end=end, file=self._stringio)

    def pushnl(self, *objects):
        self.__push(*objects, end='\n')

    def start(self):
        self.pushnl("START")

    def close(self):
        self.pushnl("DONE")

class Logger(object):
    def __init__(self, indent_string='    ', indent_level=0, *args, **kwargs):
        self.__log         = None
        self.indent_string = indent_string
        self.indent_level  = indent_level
        self.__buffer      = LogBuffer()

    @property
    def __logger(self):
        if not self.__log:
            FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
            self.__log = logging.getLogger(__name__)
            self.__log.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(logging.Formatter(FORMAT))
            self.__log.addHandler(handler)
        return self.__log

    def _log_levels(self, level):
        return {
            'debug': 10,
            'info': 20,
            'warning': 30,
            'critical': 40,
            'error': 50
        }.get(level, 'info')

    def update_indent_level(self, val):
        self.indent_level = val

    def log(self, message, color=None, log_level='info', indent_level=None, *args, **kwargs):
        msg_params = {
            'color': ColorsClass.get(color) if color is not None else ColorsClass.get("NORMAL"),
            'indent': self.indent_string * (indent_level or self.indent_level),
            'msg': message
        }
        _message = "{color} {indent}{msg}".format(**msg_params)
        self.__logger.log(self._log_levels(log_level), _message)
        self.pushbuffer(self.__buffer.prefix + _message)

    def pushbuffer(self, message):
        self.__buffer.pushnl(message)

    def start_buffer(self):
        self.__buffer.start()

    def close_buffer(self):
        self.__buffer.close()

    def getbuffer(self):
        return self.__buffer

def format_args(args, kwargs):
    """
    makes a nice string representation of all the arguments
    """
    allargs = []
    for item in args:
        allargs.append('%s' % str(item))

    for key, item in kwargs.items():
        allargs.append('%s=%s' % (key, str(item)))

    formattedArgs = ', '.join(allargs)

    if len(formattedArgs) > 150:
        return formattedArgs[:146] + " ..."
    return formattedArgs


def log_method(method, display_name=None):
    """use this for class or instance methods, it formats with the object out front."""
    display_name = display_name or method.__name__

    def _wrapper(self, *args, **kwargs):
        arg_str = format_args(args, kwargs)
        message = "{self_str}.{cls_color}{method_display_name}{method_color} ({arg_str})".format(**{
            'self_str': str(self),
            'cls_color': ColorsClass.get("BROWN"),
            'method_display_name': "{} - {}".format(method.__name__, display_name),
            'method_color': ColorsClass.get("NORMAL"),
            'arg_str': arg_str
        })
        self.log(message)
        self.logger_instance.update_indent_level(self.logger_instance.indent_level + 1)
        returnval = method(self, *args, **kwargs)
        self.logger_instance.update_indent_level(self.logger_instance.indent_level - 1)
        return returnval
    return _wrapper


def log_class(cls, log_match=".*", log_no_match="asdfnomatch", display_name=None):
    display_name = display_name or "%s" % (cls.__name__)
    names_to_check = cls.__dict__.keys()
    allow = lambda s: all([
        re.match(log_match, s),
        not re.match(log_no_match, s),
        s not in ('__str__', '__repr__')
    ])

    for name in names_to_check:
        if not allow(name):
            continue

        # unbound methods show up as mere functions in the values of
        # cls.__dict__,so we have to go through getattr
        value = getattr(cls, name)

        if isinstance(value, types.MethodType):
            # a normal instance method
            if value.im_self is None:
                setattr(cls, name, log_method(value, display_name=display_name))

            # check for cls method. class & static method are more complex.
            elif value.im_self == cls:
                _display_name = "%s.%s" % (cls.__name__, value.__name__)
                w = log_method(value.im_func, display_name=_display_name)
                setattr(cls, name, classmethod(w))
            else:
                assert False
    cls.start_logging_session()
    return cls
    
class ClassUsesLog:
    from newsline.helpers.decorators import classproperty

    singleInstance = None
    SessionPath    = ''
    LoggedClass    = ''
    DirectoryName  = ''
    __logger       = None

    @classproperty
    def logger_instance(cls):
        if not cls.__logger:
            cls.__logger = Logger()
        return cls.__logger

    def log(self, message, *args, **kwargs):
        self.logger_instance.log(message, *args, **kwargs)

    @classmethod
    def format_directoryname(cls):
        cls.LoggedClass   = str(cls.log_name).lower()
        cls.DirectoryName =  "%s_log_session_%s" % (cls.LoggedClass, formatdate(nodel=True))

        from django.conf import settings
        cls.SessionPath =  settings.LOG_FILES_STORAGE + "/" + cls.DirectoryName

    @classmethod
    def resolveInstance(cls):
        if cls.singleInstance is None:
            cls.singleInstance = cls()

        return cls.singleInstance

    @classmethod
    def start_logging_session(cls):
        cls.format_directoryname()
        cls.mkdir()
        cls.logger_instance.start_buffer()

    def close_logging_session(self):
        self.commit_logbuffer()

    def formatfilename(self):
        return "%s_logs_%s%s" % (self.LoggedClass.lower(), formatdate(nodel=True), formattime(nodel=True))

    @classmethod
    def mkdir(cls):
        import os
        from django.conf import settings
        if cls.DirectoryName is not None:
            path = settings.LOG_FILES_STORAGE + "/" + cls.DirectoryName
            if not os.path.exists(path):
                os.makedirs(path)

    def commit_logbuffer(self):
        self.logger_instance.close_buffer()
        from newsline.helpers import helpers
        filepath = self.SessionPath + "/" + self.formatfilename()
        helpers.file_put_contents(filepath, str(self.logger_instance.getbuffer()))

