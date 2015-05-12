 #-*- coding: utf-8 -*-
"""
Got that trick ^^ from http://www.python.org/dev/peps/pep-0263/

The contents of this file are subject to the PyTis Public License Version
1.1 (the "License"); you may not use this file except in compliance with
the License. You may obtain a copy of the License at
http://www.PyTis.com/License/

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
for the specific language governing rights and limitations under the
License.
"""
#import zipimport #-IMPORTNANNY
import os, shlex


import util as UTL
import util.configobj as COBJ

import wx

import logging; log=logging.getLogger('LANG-Local')

__all__ = ['language', 'languages','LanguageError']

languages = {
       'English' : 'lang.en',
       'Espa%sol' % u"\xF1".encode("mbcs") : 'lang.es',
       'Fran%sais' % u"\xE7".encode("mbcs") : 'lang.fr',
       'Deutsch' : 'lang.de',
       'Italiano' : 'lang.it',
       # XXX - TODO ADD MORE MAPPINGS
    }


class LanguageError(Exception):
    pass


class Local(object):
    current_language = None
    language = {}
    services = [] # list of service language directories
    callables = [] # list of functions to call when updating local
    debuged_callables = [] # list of labels for above list
    
    mapping=languages
    
    def __init__(self):
        """
        Returns a loaded language dict using the config obj,
        language files can be found in settings/languages
        defalut language file is settings/languages/lang.en
        
        """
        self.config = COBJ.load(UTL.paths()['config'], True)
        log.debug('initializing')
        lang_key = self.config.get('language', 'English')
        log.debug('lang_key: %s' % lang_key)
        self.setLanguage(lang_key)

    def local(self):
        log.debug('called local')
        
        for proc in self.callables:
            try:
                proc()
            except wx._core.PyDeadObjectError:
                pass
    
            
    def key(self, key, prefix=None):
        log.debug('called key')
        if not prefix:
            return key
        else:
            return "%s.%s" % (prefix,key)
                   
    def addButton(self, button_obj, label, tooltip=None):
        log.debug('called addButton')
        def proc():
            button_obj.SetLabel(self.lookup(label))
            button_obj.SetBestSize()
            return 
        if tooltip:
            self.addButtonTooltip(button_obj, tooltip)
        self.callables.append(proc)
        self.debuged_callables.append('label for button: %s' % label)
        
    def addTextCtrl(self, text_obj, data, key, label, tooltip=None):
        log.debug('called addTextCtrl')
        def proc():
            lb = self.lookup(label) 
            if lb == 'Language Key Missing: ':
                lb = ''
            text_obj.SetValue(data.get(key,lb))
            if tooltip:
                text_obj.SetLabel(self.lookup(label))
            return
            
        self.callables.append(proc)
        self.debuged_callables.append('label for StaticText: %s' % label)
        
    def addStaticText(self, text_obj, label):
        log.debug('called addStaticText')
        def proc():
            return text_obj.SetLabel(self.lookup(label))
        self.callables.append(proc)
        self.debuged_callables.append('label for StaticText: %s' % label)
        
    def addButtonTooltip(self, button_obj, label):
        log.debug('called addButtonTooltip')
        def proc():
            if hasattr(button_obj,'SetBestSize'):
                button_obj.SetBestSize()
            return button_obj.SetToolTipString(self.lookup(label))
        self.callables.append(proc)
        self.debuged_callables.append('tooltip for button: %s' % label)

    def lookup(self, label):
        
        log.debug('called lookup')
        if not label:
            return
        val = str(self.language.get(label, 'Language Key Missing: %s' % label))
        if 'Missing:' in val:
            e = "%s \n\n label = '%s'" % (os.path.abspath(os.path.join(UTL.paths()['language_dir'], self.mapping[self.current_language])), \
                                label)
            raise Exception, e
        if val.startswith('[') and val.endswith(']'):
           buf = []
           vals = shlex.split(val[1:-1])
           for i, v in enumerate(vals):
               if i == len(vals) -1:
                   buf.append(v)
               else:
                   buf.append(v[:-1])
           return buf
               
        else:
           return val

    def reverse(self, name):
        log.debug('called reverse')
        for k, v in self.language.items():
            if v == name:
                return k
        return None
    


    def setLanguage(self, lang_key):
        log.debug('called setLanguage')
        try:
            self.mapping[lang_key]
        except KeyError:
            raise LanguageError, "errors.language"
        else:
            
            self.current_language = lang_key
            path = os.path.abspath(os.path.join(UTL.paths()['language_dir'], self.mapping[self.current_language]))
            
            log.debug("Setting new Language Path: ", path)
            self.language = None
            self.language = COBJ.load(path, False)

language = Local()