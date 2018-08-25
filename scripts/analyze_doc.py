#!/usr/bin/python
# -*- coding=utf-8 -*-
#-----------------------------------------------------------------------
# Name:        Build a corpus to test and val stemmers and morphological analyzer
# Purpose:     build an advanced stemmer for Information retreival 
#  
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     2018-08-25
# Copyright:   (c) Taha Zerrouki 2018
# Licence:     GPL
#-----------------------------------------------------------------------
"""
    Build a corpus for evaluation
"""

import sys
import re
import argparse
import os
import pandas as pd
import qalsadi.analex
import pyarabic.araby as araby
import numpy as np
def grabargs():
    parser = argparse.ArgumentParser(description='Convert Quran Corpus into CSV format.')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    
    parser.add_argument("-o", dest="outfile", required=True,
    help="Output file to convert", metavar="OUT_FILE")
    #~ parser.add_argument("--dir", dest="data_directory",
    #~ help="Data directory for other external stemmers results", metavar="data_directory")
    
    parser.add_argument("--all", type=bool, nargs='?',
                        const=True, 
                        help="Test all stemmers.")
    args = parser.parse_args()
    return args

def calcul_stats(dataframe):
    """
    Calculer 
    """
    #~ df = pd.DataFrame(dataframe)
    df = dataframe
    #~ # display= data stats
    #~ print('********* ROOT ****************')
    total = df.shape[0]
    stats_list={
    "count":total,
    "uniq roots":df['root'].nunique(),
    "uniq lemmas":df['lemma'].nunique(),
    "uniq words":df['word'].nunique(),
    "mean words by root":df[['word','root']].groupby('root').count().mean(),
    "min words by root":df[['word','root']].groupby('root').count().min(),
    "max words by root":df[['word','root']].groupby('root').count().max(),
    "mean words by lemmas":df[['word','lemma']].groupby('lemma').count().mean(),
    }

    dstats = pd.DataFrame.from_dict(stats_list, orient='index')
    
    return dstats
def main():
        
    args =grabargs()
    filename = args.filename
    outfile = args.outfile
    all_stemmers = args.all
    lines =[]

    try:
        with open(filename,) as inputfile:
            for line in inputfile:
                lines.append(line.decode('utf8'))
      
    except:
        print " Can't Open the given File ", filename;
        sys.exit();
    analyzer = qalsadi.analex.Analex()
    analyzer.disable_allow_cache_use()


    #~ text = u"\n".join(lines[:10])
    text = u"\n".join(lines)
    text = araby.strip_tashkeel(text)
    text = u" ".join(araby.tokenize(text, conditions=araby.is_arabicrange))

    result = analyzer.check_text(text)
    
    adapted_result = []
    for word_analyz_list in result:
        for word_analyz in word_analyz_list :
            adapted_result.append(word_analyz.__dict__)
            
    df = pd.DataFrame(adapted_result)

    # the original word is vocalized
    # customize fields
    df['lemma'] = df['original'].apply(araby.strip_tashkeel)
    df['tag'] = df['type'].apply(lambda x: x.split(':')[0])

    # choose fields
    display = df[['word', 'root', 'lemma', 'stem','tag', 'original']]
    #join originals into one field
    dispgroup = display.groupby(['word', 'root', 'lemma', 'stem','tag'])['original'].apply(lambda x: u';'.join(list(set(list(x)))))
    dispgroup = dispgroup.drop_duplicates()
    dispgroup.to_csv(outfile,sep='\t',encoding='utf8')
    
    
    # drop duplicata
    # mmake stats on data
    display = display[['word', 'root', 'lemma', 'stem','tag']].drop_duplicates()
    x = calcul_stats(display)    
    #~ print(x)
    x.to_csv(outfile+'.stats',sep='\t',encoding='utf8')
    print("Output data is stored in %s"%outfile)
    print("Statistics data is stored in %s"%outfile+'stats')
if __name__ == '__main__':
    main()
