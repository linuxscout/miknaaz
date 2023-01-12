#!/usr/bin/python
# -*- coding=utf-8 -*-
#------------------------------------------------------------------------
# Name:        lemmatizer
# Purpose:     Arabic Lemmatizer 
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     26-08-2020
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#------------------------------------------------------------------------
"""
Syntaxic Analysis
"""

#~ from operator import xor
#~ import functools
#~ import operator
import pprint

import pyarabic.araby as araby
from qalsadi import lemmatizer
try:
    import templater 
except:
    from . import templater
    
class CorpusBuilder(lemmatizer.Lemmatizer):
    """
        Arabic Lemmatizer
    """
    def __init__(self, cache_path=False):
        """
        """
        # init corpus builder 
        super().__init__()
        
        # set vocalized lemma generation
        self.set_vocalized_lemma()
        # create analexer
        self.templater = templater.Templater()
        """Templater to extract wazns for words"""
        self.separator =";"
        """seperator between list of lemmas or roots"""
        self.join_flag = True
        """ A flag to join results as texts or return the as lists"""


        
    def __del__(self):
        pass
        
    @staticmethod
    def flatten(mylist, uniq=True):
        """
        used to flatten list of list into a list
        """
        newlist = [item for sublist in mylist for item in sublist]
        newlist = sorted(list(set(newlist)))
        return newlist

    def join(self, mylist):
        """
        return a string for given list
        """
        return self.separator.join(mylist)
        
    def set_join_flag(self, value):
        """ set A flag to join results as texts or return the as lists"""

        self.join_flag = bool(value)
        
    def set_sep(self, sep=";"):
        """Specifiy the separator to join list of lemmas or roots"""
        self.separator = sep        
        
    def morph_suggestions(self, word, to_string= True):
        """
        Generate lemmas suggestions for word, 
        This can help linguist to choose a suitable words features (lemmas, roots, types, wazns)
        
        Example:
        
        >>> text = u"إلى البيت"
        >>> result = []
        >>> lemmer = CorpusBuilder()
        >>> words = lemmer.tokenize(text)
        >>> for word in words:
        >>>     result = lemmer.morph_suggestions(word, True)
        >>>     print(result)
        {'affixes': ['---'],
         'lemmas': ['إلى'],
         'roots': [''],
         'types': ['stopword'],
         'wazns': []}
        {'affixes': ['ال---'],
         'lemmas': ['بيت'],
         'roots': ['بيت'],
         'types': ['noun'],
         'wazns': ['فعل']}

        """
        # first analyse text
        stemnodes = self.analyze_text(text=word, vocalized_lemma = True)
        
        # The analysis give us stem nodes,
        # return lemmas
        lemmas = [s.get_lemmas() for s in stemnodes]
        lemmas = self.flatten(lemmas)
        
        roots =  [s.get_roots() for s in stemnodes]  
        roots = self.flatten(roots)        
        
        affixes = [s.get_affixes() for s in stemnodes]
        # flatten affixes list
        affixes = self.flatten(affixes)
        
        # strip tashkeel
        affixes = [araby.strip_tashkeel(item) for item in affixes]
        # make uniq
        affixes = list(set(affixes))
        types = [s.get_word_type() for s in stemnodes]
        
        morph_list = [(s.get_lemmas(), s.get_roots(), s.get_word_type()) for s in stemnodes]
        wazns = self.templater.extract_wazns(morph_list)
        
        result = {"lemmas":lemmas,
                "roots":roots,
                "affixes":affixes,
               "types":types,
               "wazns":wazns,
               }  
        if to_string:
            for key in result:
                result[key] = self.join(result[key])
          
            
        
        return result

    def get_roots(self, word):
        """
        get all lemmas for word
        """
        stemnodes = self.analyze_text(text=word, vocalized_lemma = True)
        roots = [s.get_roots() for s in stemnodes]
        return roots
        
    def get_lemmas(self, word):
        """
        get all lemmas for word
        """
        stemnodes = self.analyze_text(text=word, vocalized_lemma = True)
        lemmas = [s.get_lemmas() for s in stemnodes]
        return lemmas
        
    def get_roots(self, word):
        """
        get all roots for word
        """
        stemnodes = self.analyze_text(text=word, vocalized_lemma = True)
        roots = [s.get_roots() for s in stemnodes]
     
        return roots
        
    def get_word_type(self, word):
        """
        get all lemmas for word
        """
        stemnodes = self.analyze_text(text=word, vocalized_lemma = True)
        types = [s.get_word_type() for s in stemnodes]
        return types
        
    def get_affixes(self, word):
        """
        get all lemmas for word
        """
        stemnodes = self.analyze_text(text=word, vocalized_lemma = True)
        affixes = [s.get_affixes() for s in stemnodes]
        # flatten affixes list
        affixes = self.flatten(affixes)
        # strip tashkeel
        affixes = [araby.strip_tashkeel(item) for item in affixes]
        # make uniq
        affixes = list(set(affixes))
        return affixes 
        
    def get_wazns(self, word):
        """
        get all lemmas for word
        """
        stemnodes = self.analyze_text(text=word, vocalized_lemma = True)
        lemmas_roots_list = [(s.get_lemmas(), s.get_roots(), s.get_word_type()) for s in stemnodes]
        wazns = self.templater.extract_wazns(lemmas_roots_list)
        return wazns
        
    def get_wazns(self, word):
        """
        get all lemmas for word
        """
        stemnodes = self.analyze_text(text=word, vocalized_lemma = True)
        lemmas_roots_list = [(s.get_lemmas(), s.get_roots(), s.get_word_type()) for s in stemnodes]
        wazns = self.templater.extract_wazns(lemmas_roots_list)
        return wazns
        
    def tokenize(self, text):
        """ retrun tokens from given text"""
        return araby.tokenize(text)
       
            

def mainly():
    """
    main test
    """
    # #test syn
    result = []
    text = u"إلى البيت"
    lemmer = CorpusBuilder()
    words = lemmer.tokenize(text)
    for word in words:
        result = lemmer.morph_suggestions(word, True)
        # the result contains objects
        pprint.pprint(result)
    # test get lemmas
    for word in words:
        result = lemmer.get_lemmas(word)
        # the result contains objects
        print(result)
    # test get roots
    for word in words:
        result = lemmer.get_roots(word)
        # the result contains objects
        print(result)
    # test get wordtypes
    for word in words:
        result = lemmer.get_word_type(word)
        # the result contains objects
        print(result)
    # test get wazns
    for word in words:
        result = lemmer.get_wazns(word)
        # the result contains objects
        print(result)

if __name__ == "__main__":
    mainly()

