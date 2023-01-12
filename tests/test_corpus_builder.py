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

sys.path.append("../")
from miknaaz.corpus_builder import CorpusBuilder

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
    "uniq roots":df['roots'].nunique(),
    "uniq lemmas":df['lemmas'].nunique(),
    "uniq words":df['word'].nunique(),
    "mean words by root":df[['word','roots']].groupby('roots').count().mean(),
    # ~ "min words by root":df[['word','root']].groupby('root').count().min(),
    "max words by root":df[['word','roots']].groupby('roots').count().max(),
    "mean words by lemmas":df[['word','lemmas']].groupby('lemmas').count().mean(),
    }

    dstats = pd.DataFrame.from_dict(stats_list, orient='index')
    
    return dstats
    
def main():
        
    args =grabargs()
    filename = args.filename
    outfile = args.outfile
    all_stemmers = args.all
    lines =[]
    # read data
    df = pd.read_csv(filename, encoding="utf8", delimiter="\t")
    # fill nan
    df.fillna("", inplace=True)
    print(df.shape)
    print(df.head(20))

    lemmer = CorpusBuilder()
    # add word features into each row
    df2 = df.merge(df['word'].apply(lambda s: pd.Series(lemmer.morph_suggestions(s))), 
    left_index=True, right_index=True)
    
    print(df2)
    df2.to_csv(outfile ,sep='\t',encoding='utf8')    
    x = calcul_stats(df2)  
    print(x)
    x.to_csv(outfile+'.stats',sep='\t',encoding='utf8')
    print("Output data is stored in %s"%outfile)
    print("Statistics data is stored in %s"%outfile+'.stats')
if __name__ == '__main__':
    main()
