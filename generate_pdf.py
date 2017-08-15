#!/usr/bin/env python

import sys, os, re, argparse, glob, subprocess
import fnmatch


def find_files(directory, pattern='*'):
    if not os.path.exists(directory):
        raise ValueError("Directory not found {}".format(directory))

    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            if fnmatch.filter([full_path], pattern):
                matches.append(os.path.join(root, filename))
    return matches



if __name__ == "__main__":
    path = os.path.dirname(os.path.realpath(__file__))

    parser = argparse.ArgumentParser()
    parser.add_argument("--gcbias-files", required=True)
    parser.add_argument("--globdir", required=True)
    parser.add_argument("--mdmetrics-files", required=True)
    parser.add_argument("--insertsize-files", required=True)
    parser.add_argument("--hsmetrics-files", required=True)
    parser.add_argument("--qualmetrics-files", required=True)
    parser.add_argument("--fingerprint-files", required=True)
    parser.add_argument("--trimgalore-files", required=True)
    parser.add_argument("--file-prefix", required=True)
    parser.add_argument("--fp-genotypes", required=True)
    parser.add_argument("--pairing-file", required=True)
    parser.add_argument("--grouping-file", required=True)
    parser.add_argument("--request-file", required=True)
    args = parser.parse_args()
    path_to_search = "/".join(args.globdir.split("/")[:-1])
    print "Search path: %s" % path_to_search
    datapath = os.path.dirname(os.path.realpath(args.request_file))
    print >>sys.stderr, "Generating merged picard metrics (GC Bias, Mark Dups, Hs Metrics)..."
    outfilenames = [ args.file_prefix + "_GcBiasMetrics.txt", args.file_prefix + "_markDuplicatesMetrics.txt", args.file_prefix + "_HsMetrics.txt"]
    for i, files in enumerate([args.gcbias_files, args.mdmetrics_files, args.hsmetrics_files]):
        temp_fh = open("temp_fof", "wb")
        filenames = find_files(path_to_search, pattern=files)
        for name in filenames:
            print name
            temp_fh.write(name + "\n")
        temp_fh.close()
        cmd = ["perl", os.path.join(path, "mergePicardMetrics.pl"), "-files", "temp_fof", ">", outfilenames[i]]
        print >>sys.stderr, " ".join(cmd)
        subprocess.call(" ".join(cmd), shell=True)
    print >>sys.stderr, "Generated GcBias, MarkDuplicate, and HsMetrics inputs without error"
    print >>sys.stderr, "Generating Insert Size Histogram..."
    temp_fh = open("temp_fof", "wb")
    filenames = find_files(path_to_search, pattern=args.insertsize_files)
    for name in filenames:
        print name
        temp_fh.write(name + "\n")
    temp_fh.close()

    cmd = ['python', os.path.join(path,'mergeInsertSizeHistograms.py'), 'temp_fof', args.file_prefix + "_InsertSizeMetrics_Histograms.txt" ]
    print >>sys.stderr, " ".join(cmd)
    rv = subprocess.call(cmd, shell=False)
    if rv !=0:
        print >>sys.stderr, "Error Generating IS hist"
        sys.exit(1)
    print >>sys.stderr, "Insert Size Histogram Generated!"
    print >>sys.stderr, "Generating Fingerprint from DOC inputs..."
    temp_fh = open("temp_fof", "wb")
    filenames = find_files(path_to_search, pattern=args.fingerprint_files)
    for name in filenames:
        temp_fh.write(name + "\n")
    temp_fh.close()
    cmd = ['python', os.path.join(path, 'analyzeFingerprint.py'), '-pre', args.file_prefix, '-fp', args.fp_genotypes, 
            '-group', args.grouping_file, '-outdir', '.', '-pair', args.pairing_file, "-fof", 'temp_fof']
    print >>sys.stderr, " ".join(cmd)
    rv = subprocess.call(cmd, shell=False)
    if rv !=0:
        print >>sys.stderr, "Error Generating fingerprint..."
        sys.exit(1)
    print >>sys.stderr, "Fingerprint File Generated!"
    print >>sys.stderr, "Generating Qual Files..."
    temp_fh = open("temp_fof", "wb")
    filenames = find_files(path_to_search, pattern=args.qualmetrics_files)
    for name in filenames:
        temp_fh.write(name + "\n")
    temp_fh.close()
    cmd = ['python', os.path.join(path, 'mergeMeanQualityHistograms.py'), 'temp_fof', args.file_prefix + "_post_recal_MeanQualityByCycle.txt", args.file_prefix + "_pre_recal_MeanQualityByCycle.txt"]
    print >>sys.stderr, " ".join(cmd)
    rv = subprocess.call(cmd, shell=False)
    if rv !=0:
        print >>sys.stderr, "Error Generating Mean Quality..."
        sys.exit(1)
    print >>sys.stderr, "Qual Files Generated!"
    print >>sys.stderr, "Generating CutAdapt Summary.."
    temp_fh = open("temp_fof", "wb")
    filenames = find_files(path_to_search, pattern=args.trimgalore_files)
    for name in filenames:
        print name
        temp_fh.write(name + "\n")
    temp_fh.close()
    cmd = ['python', os.path.join(path,'mergeCutAdaptStats.py'), 'temp_fof', args.file_prefix + "_CutAdaptStats.txt"]
    print >>sys.stderr, cmd
    rv = subprocess.call(cmd, shell=False)
    if rv !=0:
        print >>sys.stderr, "Error Generating PDF..."
        sys.exit(1)

    print >>sys.stderr, "CutadaptSummary Generated!"
    print >>sys.stderr, "GENERATING THE GOSH DARN PDF!"
    cmd = ['perl', os.path.join(path, 'qcPDF.pl'), '-pre', args.file_prefix, '-path', '.', '-log', 'qcPDF.log', '-request', args.request_file, '-version', '1.0']
    print >>sys.stderr, " ".join(cmd)
    rv = subprocess.call(cmd, shell=False)
    if rv !=0:
        print >>sys.stderr, "Error Generating PDF..."
        sys.exit(1)
    print >>sys.stderr, "PDF Generated!"
    



