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
    bigdf = pd.DataFrame(columns = ['sample','value'])
    if not mcSampleList:
        bigdf.to_csv(args.project_prefix+'_MinorContamFreqList.txt', index=False, sep='\t')
    else:
        for sample in mcSampleList:
            subsetdf = fp[(fp[sample+'_MinorAlleleFreq'] > 0.0) & (fp[sample+'_MinorAlleleFreq'] <= 0.1)][[sample+'_Genotypes', sample+'_MinorAlleleFreq',sample+'_Counts']] #added >=
            # df['vartype'] = df['variant_id'].apply(lambda x: x[0:3])
            subsetdf['sample'] = sample
            # subsetdf['newcounts'] = subsetdf[sample+'_Counts'].apply(lambda x: int(x.split(' ')[0].split(':')[1]) + int(x.split(' ')[1].split(':')[1]))
            # subsetdf = subsetdf.loc[subsetdf['newcounts'] >= 100]  # make sure each variant_id has two instances
            subsetdf = subsetdf[['sample',sample+'_MinorAlleleFreq']]
            subsetdf.columns = ['sample','value']
            bigdf = pd.concat([bigdf,subsetdf],axis=0)
        bigdf.to_csv(args.project_prefix+'_MinorContamFreqList.txt',index=False,sep='\t')
