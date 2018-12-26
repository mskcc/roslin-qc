#!/usr/bin/env python

import pandas as pd
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--minorcontam', required=True, help='Project level minor contamination file. ie Proj_06604_G_MinorContamination.txt')
    parser.add_argument('--fpsummary', required=True, help='Project level fingerprint summary, ie Proj_06604_G_FingerprintSummary.txt')
    parser.add_argument('--min_cutoff', required=False, default=0.01, type=float, help='minimum cutoff for minor contam frequency to be detected, default value is 0.01')
    parser.add_argument('--project_prefix', required=True, help='Project name, ie Proj_000001_A')
    args = parser.parse_args()

    mc = pd.read_csv(args.minorcontam,sep='\t')
    mcSampleList = list(mc.loc[mc['AvgMinorHomFreq']>=args.min_cutoff]['Sample'])

    fp = pd.read_csv(args.fpsummary, sep='\t')
    bigdf = pd.DataFrame()
    for sample in mcSampleList:
        subsetdf = fp[(fp[sample+'_MinorAlleleFreq'] > 0.0) & (fp[sample+'_MinorAlleleFreq'] <= 0.1)][[sample+'_Genotypes', sample+'_MinorAlleleFreq']]
        subsetdf['sample'] = sample
        subsetdf = subsetdf[['sample',sample+'_MinorAlleleFreq']]
        subsetdf.columns = ['sample','value']
        bigdf = pd.concat([bigdf,subsetdf],axis=0)
    bigdf.to_csv(args.project_prefix+'_MinorContamFreqList.txt',index=False,sep='\t')
