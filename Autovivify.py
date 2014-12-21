#!/usr/bin/python

#--------------------------------------------------------------
# This is intended to mimic the Autovivification feature of Perl
# It will be able to create n deep dictionaries with a specified 
# data type in the inner most value 
#
# E.g. import Autovivify
# some_dict=Autovivify.construct(3, list) 
# will create a 3 level deep (i.e. 3 sets of keys) dictionary
# with a list as the innermost value 
#--------------------------------------------------------------

from collections import defaultdict

def construct(levels, final_type):
    return(defaultdict(final_type) if levels<2 else 
          defaultdict(lambda: construct(levels-1,final_type)))

