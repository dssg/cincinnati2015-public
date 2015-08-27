#!/usr/bin/env python

land_uses = ["single_family", "two_family", "three_family", "multi_family", "mixed_use"]
dfns = {"tax_foreclosure": ["years_taxforeclosure_since3yrs", "imputation_years_taxforeclosure_since3yrs"], 
              "mean_market_value": ["mean_market_value_3yrs", "imputation_mean_market_value_3yrs"], 
              "change_market_value": ["change_market_value_3yrs", "imputation_change_market_value_3yrs"],
              "mean_impr_value": ["mean_impr_value_3yrs", "imputation_mean_impr_value_3yrs"], 
              "change_impr_value": ["change_impr_value_3yrs", "imputation_change_impr_value_3yrs"],
              "mean_land_value": ["mean_land_value_3yrs", "imputation_mean_land_value_3yrs"], 
              "change_land_value": ["change_land_value_3yrs", "imputation_change_land_value_3yrs"],
              "home_use": land_uses, 
              "owner_ner": ["owner_ner"]}

insp_years = ['20' + str(x).zfill(2) for x in range(5, 16)]

forcl_three_yrs_back = {'2005': None,
                      '2006': None,
                      '2007': None,
                      '2008': ['forcl_flag2007'],
                      '2009': ['forcl_flag2007', 'forcl_flag2008'],
                      '2010': ['forcl_flag2007', 'forcl_flag2008', 'forcl_flag2009'],
                      '2011': ['forcl_flag2008', 'forcl_flag2009', 'forcl_flag2010'],
                      '2012': ['forcl_flag2009', 'forcl_flag2010', 'forcl_flag2011'],
                      '2013': ['forcl_flag2010', 'forcl_flag2011', 'forcl_flag2012'],
                      '2014': ['forcl_flag2011', 'forcl_flag2012', 'forcl_flag2013'],
                      '2015': ['forcl_flag2012', 'forcl_flag2013', 'forcl_flag2014']}

total_val_three_yrs_back = {'2005': None,
                      '2006': None,
                      '2007': None,
                      '2008': ['mkt_total_val2007'],
                      '2009': ['mkt_total_val2007', 'mkt_total_val2008'],
                      '2010': ['mkt_total_val2007', 'mkt_total_val2008', 'mkt_total_val2009'],
                      '2011': ['mkt_total_val2008', 'mkt_total_val2009', 'mkt_total_val2010'],
                      '2012': ['mkt_total_val2009', 'mkt_total_val2010', 'mkt_total_val2011'],
                      '2013': ['mkt_total_val2010', 'mkt_total_val2011', 'mkt_total_val2012'],
                      '2014': ['mkt_total_val2011', 'mkt_total_val2012', 'mkt_total_val2013'],
                      '2015': ['mkt_total_val2012', 'mkt_total_val2013', 'mkt_total_val2014']}

impr_val_three_yrs_back = {'2005': None,
                      '2006': None,
                      '2007': None,
                      '2008': ['mkt_impr_val2007'],
                      '2009': ['mkt_impr_val2007', 'mkt_impr_val2008'],
                      '2010': ['mkt_impr_val2007', 'mkt_impr_val2008', 'mkt_impr_val2009'],
                      '2011': ['mkt_impr_val2008', 'mkt_impr_val2009', 'mkt_impr_val2010'],
                      '2012': ['mkt_impr_val2009', 'mkt_impr_val2010', 'mkt_impr_val2011'],
                      '2013': ['mkt_impr_val2010', 'mkt_impr_val2011', 'mkt_impr_val2012'],
                      '2014': ['mkt_impr_val2011', 'mkt_impr_val2012', 'mkt_impr_val2013'],
                      '2015': ['mkt_impr_val2012', 'mkt_impr_val2013', 'mkt_impr_val2014']}

land_val_three_yrs_back = {'2005': None,
                      '2006': None,
                      '2007': None,
                      '2008': ['mkt_land_val2007'],
                      '2009': ['mkt_land_val2007', 'mkt_land_val2008'],
                      '2010': ['mkt_land_val2007', 'mkt_land_val2008', 'mkt_land_val2009'],
                      '2011': ['mkt_land_val2008', 'mkt_land_val2009', 'mkt_land_val2010'],
                      '2012': ['mkt_land_val2009', 'mkt_land_val2010', 'mkt_land_val2011'],
                      '2013': ['mkt_land_val2010', 'mkt_land_val2011', 'mkt_land_val2012'],
                      '2014': ['mkt_land_val2011', 'mkt_land_val2012', 'mkt_land_val2013'],
                      '2015': ['mkt_land_val2012', 'mkt_land_val2013', 'mkt_land_val2014']}