#!/usr/bin/env python

import pandas as pd
import numpy as np
import glob
import os
import argparse

if __name__ == '__main__':
    pd.options.mode.chained_assignment = None  # default='warn'

    parser = argparse.ArgumentParser(add_help= True, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--pairing_file',required=True,help='Pairing file')
    parser.add_argument('--fillout_file',required=True,help='Fillout portal file from cmo_fillout')
    parser.add_argument('--project_prefix', required=True,help='Project name, ie Proj_000001_A')
    args = parser.parse_args()

    pairinglist = []
    tumor_list = []
    norm_list = []
    with open(args.pairing_file, 'r') as f:
        for line in f:
            line = line.strip()
            normal,tumor = line.split('\t')
            if 'pool' in normal.lower():
                pass
            else:
                norm_list.append(normal)
                tumor_list.append(tumor)
                pairinglist.append(tumor+'_vs_'+normal)

    df = pd.read_csv(args.fillout_file, sep='\t')
    df['tn'] = df['Tumor_Sample_Barcode'].apply(lambda x: 'normal' if x in norm_list else('tumor' if x in tumor_list else 'error'))

    counter = 0
    for pair in pairinglist:
        tumor,normal = pair.split("_vs_")
        subsetdf = df.loc[df['Tumor_Sample_Barcode'].isin([tumor,normal])]
        if not subsetdf.empty:
            # print subsetdf
            print pair
            subsetdf['root'] = pair
            subsetdf['snv'] = subsetdf.apply(lambda x:'%s_%s_%s_%s_%s_%s' % (x['root'],x['Hugo_Symbol'],x['Chromosome'],x['Start_Position'],x['Tumor_Seq_Allele1'],x['Tumor_Seq_Allele2']),axis=1)
            subsetdf['geneaa'] = subsetdf.apply(lambda x:'%s:%s' % (x['Hugo_Symbol'],x['HGVSp_Short']),axis=1)
            subsetdf['t_variant_frequency'] = subsetdf['t_alt_count']/subsetdf['t_depth']
            normal_only = subsetdf.loc[subsetdf['tn'] == 'normal']
            normal_only = normal_only.loc[(normal_only['t_variant_frequency'] >= 0.02) & (normal_only['t_depth'] >= 20) & (normal_only['t_alt_count'] > 2)]  # inlcude normal alt depth > 2
            norm_top10 = normal_only.sort_values('t_variant_frequency', ascending=False).groupby('Tumor_Sample_Barcode').head(10)

            shortlist = ['Hugo_Symbol',
            'root',
            'tn',
            'geneaa',
            'Chromosome',
            'Start_Position',
            'End_Position',
            'Variant_Classification',
            'Variant_Type',
            'Reference_Allele',
            'Tumor_Sample_Barcode',
            't_ref_count',
            't_alt_count',
            't_depth',
            't_variant_frequency']

            curated = list(norm_top10['snv'].unique())
            subsetdf = subsetdf.loc[subsetdf['snv'].isin(curated)]
            subsetdf.loc[subsetdf['t_depth'] < 20, 't_variant_frequency'] = 0
            subsetdf = subsetdf[shortlist]
            subsetdf['counts'] = subsetdf['t_alt_count'].astype(str) + '/' + subsetdf['t_depth'].astype(str)
            if counter == 0:
                counter+=1
                subsetdf.to_csv('%s_HotspotsInNormals.txt' % args.project_prefix, index=False, sep='\t')
            else:
                subsetdf.to_csv('%s_HotspotsInNormals.txt' % args.project_prefix, mode='a', header=False, index=False, sep='\t')
