from pylatex import Document, Section, Command, Figure, NewPage, Tabular, LongTabu, MultiColumn, MultiRow, Table
from pylatex.package import Package
from pylatex.utils import NoEscape, bold, escape_latex
import glob,os
import pandas as pd
import fnmatch
import argparse
import re

def textsf(s):
    return NoEscape(r'\textsf{' + s + '}')

def colorcellStatus(autostatus,colortext):
    if colortext == 'color':
        cellstr = ''
    elif colortext == 'text':
        cellstr = autostatus
    # NoEscape(r'\cellcolor{yellow}'+row["AutoStatus"]))
    if autostatus.upper() == 'FAIL':
        return NoEscape(r'\cellcolor{red}'+cellstr)
    elif autostatus.upper() == 'PASS':
        return NoEscape(r'\cellcolor{green}'+cellstr)
    elif autostatus.upper() == 'WARN':
        return NoEscape(r'\cellcolor{yellow}'+cellstr)


def count_pages(filename):
    rxcountpages = re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE|re.DOTALL)
    data = file(filename,"rb").read()
    return len(rxcountpages.findall(data))

def colorcellCoverage(coverage,colortext):
    if colortext == 'color':
        cellstr = ''
    elif colortext == 'text':
        cellstr = str(coverage)
    coverage = int(coverage)

    # NoEscape(r'\cellcolor{yellow}'+row["AutoStatus"]))
    if coverage < 50:
        return NoEscape(r'\cellcolor{red}'+cellstr)
    elif coverage <= 200:
        return NoEscape(r'\cellcolor{yellow}'+cellstr)
    elif coverage > 200:
        return NoEscape(r'\cellcolor{green}'+cellstr)

def go_to_toc(doc):
    doc.append(NoEscape(r'\normalsize'))
    doc.append(NoEscape(r'\textsf{Go to \hyperlink{toc}{Table of Contents}}'))

def create_file_dict(filename):
    file_dict = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            linelist = line.split(':')
            if len(linelist) > 2:
                k = linelist[0].strip()
                v = ':'.join(linelist[1:]).strip()
            else:
                k = linelist[0].strip()
                v = linelist[1].strip()
            file_dict[k] = v
    return file_dict


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--full_project_name", required=True, help="project name, ie Proj_DEV_0003")
    parser.add_argument("--path", required=True, help="Directory containing paths; typically called 'consolidated_metrics_data'")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--request_file", help="full path to request file (ie Proj_CobiTrial_2019_request.txt)")
    group.add_argument("--assay", help="assay name")
    parser.add_argument("--pi", help="PI name (must be used with --assay)")
    parser.add_argument("--pi_email", help="PI email (must be used with --assay)")
    args = parser.parse_args()
    requestdict = {}
    if args.assay:
        if not args.pi:
            print("Error: value for PI is not specified")
            exit(1)
        if not args.pi_email:
            print("Error: value for PI_email not specified")
            exit(1)
        requestdict['Assay'] = args.assay.strip()
        requestdict['PI'] = args.pi.strip()
        requestdict['PI_E-mail'] = args.pi_email.strip()
    else:
        requestdict = create_file_dict(args.request_file)
    pdfpath = args.path
    proj = escape_latex(args.full_project_name)
    projfile = os.path.join(args.path, args.full_project_name+'_ProjectSummary.txt')
    samplefile = os.path.join(args.path, args.full_project_name+'_SampleSummary.txt')
    geometry_options = {"tmargin": "1cm", "bmargin": "2cm", "lmargin": "1cm", "rmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)
    doc.documentclass = Command(
        'documentclass',
        options=['10pt', 'landscape'],
        lmodern=True,
        arguments=['article'],
        fontenc='T1',
    )
    doc.preamble.append(NoEscape(r'\hypersetup{'
                        r'colorlinks=true,'
                        r'linkcolor=blue,'
                        r'anchorcolor=blue,'
                        r'citecolor=blue,'
                        r'filecolor=blue,'
                        r'urlcolor=blue,}'))

    #LOADING PACKAGES
    doc.packages.append(Package('hyperref'))
    doc.packages.append(Package('csvsimple'))
    doc.packages.append(Package('colortbl'))
    doc.packages.append(Package('caption'))
    doc.packages.append(Package('tgheros'))
        # doc.packages.append(Package('secsty'))
    # doc.packages.append(Package('tocloft'))
    # \renewcommand{\cftchapfont}{\normalfont\sffamily}
    # \renewcommand{\cftsecfont}{\normalfont\sffamily}
    doc.append(NoEscape(r'\renewcommand{\familydefault}{\sfdefault}'))
    doc.append(NoEscape(r'\captionsetup{labelsep=period}'))


    doc.append(NoEscape(r'\begin{titlepage}'))
    doc.append(NoEscape(r'\begin{center}'))
    doc.append(NoEscape(r'\vspace{1cm}'))
    doc.append(NoEscape(r'\LARGE'))
    doc.append(NoEscape(r'\textbf{\textsf{Center for Molecular Oncology}}\\'))
    doc.append(NoEscape(r'\textbf{\textsf{Memorial Sloan Kettering Cancer Center}}\\'))



    doc.append(NoEscape(r'\vspace{5.0cm}'))
    doc.append(NoEscape(r'\LARGE'))
    doc.append(NoEscape(r'\textbf{\textsf{Project %s}}\\' % proj))
    doc.append(NoEscape(r'\textbf{\textsf{QC Metrics Report}}\\'))
    doc.append(NoEscape(r'\vspace{3.5cm}'))
    # doc.append(NoEscape(r'\textbf{Author Name}\\'))
    # request dict
    # assaytype
    doc.append(NoEscape(r'\textbf{\textsf{Roslin 2.5}}\\'))

    doc.append(NoEscape(r'\vspace{2.5cm}'))

    doc.append(NoEscape(r'\textsf{Assay: %s}\\' % escape_latex(requestdict['Assay'])))
    doc.append(NoEscape(r'\textsf{PI: %s}\\' % escape_latex(requestdict['PI'])))
    doc.append(NoEscape(r'\textsf{PI email: %s}\\' % escape_latex(requestdict['PI_E-mail'])))

    doc.append(NoEscape(r'\vfill'))
    doc.append(NoEscape(r'\end{center}'))
    doc.append(NoEscape(r'\end{titlepage}'))


    doc.append(NewPage())
    doc.append(NoEscape(r'\large'))
    doc.append(NoEscape(r'\hypertarget{toc}{}'))
    doc.append(NoEscape(r'\tableofcontents'))
    doc.append(NoEscape(r'\renewcommand{\familydefault}{\sfdefault}'))


    doc.append(NewPage())
    doc.append(NoEscape(r'\section{Project Summary}'))

    go_to_toc(doc)
    doc.append(NoEscape(r'\footnotesize'))
    projdf = pd.read_csv(projfile, sep='\t')
    projdf = projdf.replace(pd.np.nan,'',regex=True)

    sampdf = pd.read_csv(samplefile, sep='\t')
    sampdf = sampdf.replace(pd.np.nan, '', regex=True)
    doc.append(NoEscape(r'\renewcommand{\familydefault}{\sfdefault}'))

    with doc.create(LongTabu("|c|l|c|X[p]|c|X[m]|", row_height=1.5)) as data_table:
        header_row1 = ["AutoStatus", "Metric", "Category", "Summary Description", "Summary Value", "Failures"]
        data_table.add_hline()
        data_table.add_row(header_row1,mapper=[bold,textsf])
        data_table.add_hline()

        for index, row in projdf.iterrows():
            # if row['Metric'] == 'Cluster Density':
            if index == 0: ## Cluster Density
                prow = row.tolist()
                data_table.add_row((MultiRow(2,data=colorcellStatus(row['AutoStatus'],'color')),MultiRow(2,data=row['Metric']),prow[2],prow[3],prow[4],prow[5] ),mapper=textsf)
                data_table.add_hline(3,6)
            elif index == 1:
                prow = row.tolist()
                data_table.add_row((MultiRow(NoEscape(-2),data=colorcellStatus(row['AutoStatus'],'text')),MultiRow(2,data=''),prow[2],prow[3],prow[4],prow[5] ),mapper=textsf)
                data_table.add_hline()
            elif index == 3: ## Capture Specificity (skipping index 2 because its formatted weird..)
                prow = row.tolist()
                data_table.add_row((MultiRow(3, data=colorcellStatus(row['AutoStatus'], 'color')), MultiRow(3, data=row['Metric']), MultiRow(3, data=''), prow[3], prow[4], prow[5]), mapper=textsf)
                data_table.add_hline(4,6)
            elif index == 4:
                prow = row.tolist()
                data_table.add_row((MultiRow(3, data=colorcellStatus(row['AutoStatus'], 'color')), MultiRow(3, data=''), MultiRow(3, data=''), prow[3], prow[4], prow[5]),mapper=textsf)
                data_table.add_hline(4, 6)
            elif index == 5:
                prow = row.tolist()
                data_table.add_row((MultiRow(NoEscape(-3), data=colorcellStatus(row['AutoStatus'], 'text')), MultiRow(3, data=''), MultiRow(3, data=''), prow[3], prow[4], prow[5]), mapper=textsf)
                data_table.add_hline()
            elif index == 7: #Insert Size, index 6 not used?!
                prow = row.tolist()
                data_table.add_row(colorcellStatus(prow[0], 'text'), prow[1], prow[2], prow[3], prow[4], prow[5], mapper=textsf)
                data_table.add_hline()
            elif index == 8: # Sample Labeling Errors
                prow = row.tolist()
                data_table.add_row((MultiRow(2, data=colorcellStatus(row['AutoStatus'],'color')), MultiRow(2, data=NoEscape(row['Metric']),width='2.5cm'), prow[2], prow[3], prow[4], prow[5]),mapper=textsf)
                data_table.add_hline(3, 6)
            elif index == 9:
                prow = row.tolist()
                data_table.add_row((MultiRow(NoEscape(-2), data=colorcellStatus(row['AutoStatus'], 'text')), MultiRow(2, data=''), prow[2], prow[3], prow[4], prow[5]), mapper=textsf)
                data_table.add_hline()
            elif index == 10: # Contamination
                prow = row.tolist()
                # data_table.add_row((MultiRow(2, data=row['AutoStatus']), MultiRow(2, data=NoEscape(r'{\parbox{10cm}{'+row['Metric']+'}}')), prow[2], prow[3], prow[4], prow[5]))
                data_table.add_row((MultiRow(3, data=colorcellStatus(row['AutoStatus'], 'color')), MultiRow(3, data=NoEscape(row['Metric'])), prow[2], prow[3], prow[4], prow[5]), mapper=textsf)
                data_table.add_hline(3, 6)
            elif index == 11:
                prow = row.tolist()
                data_table.add_row((MultiRow(3, data=colorcellStatus(row['AutoStatus'], 'color')), MultiRow(3, data=''), prow[2], prow[3], prow[4], prow[5]),mapper=textsf)
                data_table.add_hline(3,6)
            elif index == 12:
                prow = row.tolist()
                data_table.add_row((MultiRow(NoEscape(-3), data=colorcellStatus(prow[0], 'text')), MultiRow(3, data=''), prow[2], prow[3], prow[4], prow[5]),mapper=textsf)
                data_table.add_hline()
            elif index == 13: #Duplication
                prow = row.tolist()
                data_table.add_row(colorcellStatus(prow[0], 'text'), prow[1], prow[2], prow[3], prow[4], prow[5], mapper=textsf)
                data_table.add_hline()
            elif index == 14: #Library Size
                prow = row.tolist()
                data_table.add_row(colorcellStatus(prow[0], 'text'), prow[1], prow[2], prow[3], prow[4], prow[5], mapper=textsf)
                data_table.add_hline()
            elif index == 15:  # Target Coverage
                prow = row.tolist()
                data_table.add_row((MultiRow(3, data=colorcellStatus(row['AutoStatus'], 'color')), MultiRow(3, data=NoEscape(row['Metric'])), prow[2], prow[3], prow[4], prow[5]), mapper=textsf)
                data_table.add_hline(3, 6)
            elif index == 16:
                prow = row.tolist()
                data_table.add_row((MultiRow(3, data=colorcellStatus(row['AutoStatus'], 'color')), MultiRow(3, data=''), prow[2], prow[3], prow[4], prow[5]),mapper=textsf)
                data_table.add_hline(3, 6)
            elif index == 17:
                prow = row.tolist()
                data_table.add_row((MultiRow(NoEscape(-3), data=colorcellStatus(prow[0], 'text')), MultiRow(3, data=''), prow[2], prow[3], prow[4], prow[5]), mapper=textsf)
                data_table.add_hline()

    doc.append(NewPage())
    doc.append(NoEscape(r'\section{Sample Summary}'))
    go_to_toc(doc)
    doc.append(NoEscape(r'\footnotesize'))

    # with doc.create(LongTabu("|X[c]|X[c]|X[p]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|", row_height=1.5)) as data_table:
    with doc.create(LongTabu(r"|c|l|l|l|X[c]|X[c]|X[c]|X[c]|m{1cm}|>{\raggedright}m{1cm}|m{1cm}|X[c]|m{1cm}|", row_height=2.5)) as data_table:
        header_row1 = ["Status","Tumor Sample Barcode","Unexpected Match","Unexpected Mismatch","Major Contam.","Minor Contam.","Coverage","Duplication","Library Size (millions)","On Bait Bases (millions)","Aligned Reads (millions)","Insert Size Peak","% Trimmed Reads"]
        data_table.add_hline()
        # doc.append(NoEscape(r'\rowfont{\tiny}'))
        data_table.add_row(header_row1, mapper=[bold,textsf])
        data_table.end_table_header()

        data_table.add_hline()
        for index, row in sampdf.iterrows():
            # if row['Metric'] == 'Cluster Density':
            # if index == 0:  # Cluster Density
            if index == 0:
                prow = row.tolist()
                # data_table.add_row(prow)
                data_table.add_row((MultiRow(1, data=prow[0]), prow[1], prow[2], prow[3], prow[4], prow[5], prow[6], prow[7], prow[8], prow[9], prow[10], prow[11], prow[12]), mapper=textsf)
                data_table.add_hline()
            else:
                prow = row.tolist()
                # data_table.add_row(prow)
                data_table.add_row((MultiRow(1, data=colorcellStatus(prow[0], 'text')), prow[1], prow[2], prow[3], prow[4], prow[5],MultiRow(1,data=colorcellCoverage(prow[6],'text')),  prow[7], prow[8], prow[9], prow[10], prow[11], prow[12]),mapper=textsf)
                data_table.add_hline()
        # data_table.add_hline(2, 3)
        # data_table.add_row(('', 3, 4))
        # data_table.add_hline(2, 3)
        # data_table.add_row(('', 5, 6))
        # data_table.add_hline()
        # data_table.add_row((MultiRow(3, data='Multirow2'), '', ''))
        # data_table.add_empty_row()
        # data_table.add_empty_row()
        # data_table.add_hline()

        # data_table.append(NoEscape(r'\csvreader[separator=tab, head to column names]{'+projfile+'}{}'))
        # data_table.append(NoEscape(r'{\\\AutoStatus & \Metric & \Category & \SummaryDescription & \SummaryValue & \Failures}'))
        # data_table.append(NoEscape(r'\\\hline'))
        # data_table.append(NoEscape(r'\rhi'))
        # data_table.append(NoEscape(r'\rhi'))

    # doc.append(NoEscape(r'\begin{table}'))
    # doc.append(NoEscape(r'\csvloop{'
    #             r'file=files/Proj_DEV_0003_ProjectSummary.txt,'
    #             r'separator=tab}'))
    # doc.append(NoEscape(r'\end{table}'))


    doc.append(NewPage())
    doc.append(NoEscape(r'\normalsize'))
    #this will be tied to qc_summary.R
    scalewidth = NoEscape(r'.79\textwidth')
    small_scalewidth = NoEscape(r'.6\textwidth')
    pdfgloblist = glob.glob(os.path.join(pdfpath, '*.pdf'))
    pdfgloblist.extend(glob.glob(os.path.join(pdfpath, '*.txt')))
    # numlist = [0,12,4,14,11,3,9,2,8,1,13,10,5,6,7]
    # pdflist = [pdfgloblist[current_index] for current_index in numlist]

    # for pdfimg in pdflist:
    for pdfimg in pdfgloblist:
        if pdfimg.endswith('_alignment.pdf'):
            doc.append(NoEscape(r'\section{Cluster Density \& Alignment Rate}'))
            go_to_toc(doc)
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                numclusters = str(int(projdf['SummaryValue'][0]))
                pctalign = str(projdf['SummaryValue'][1]*100)
                qc_fig.add_caption(NoEscape(r'Cluster Density: There were a total of %s million clusters on the lane. %s\%% of these had both reads align to the reference genome.' % (numclusters,pctalign)))
            doc.append(NewPage())
        elif pdfimg.endswith('_alignment_percentage.pdf'):
            doc.append(NoEscape(r'\section{Cluster Density \& Alignment Rate Relative Percentage}'))
            go_to_toc(doc)
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                numclusters = str(int(projdf['SummaryValue'][0]))
                pctalign = str(projdf['SummaryValue'][1]*100)
                qc_fig.add_caption(NoEscape(r'Cluster Density: There were a total of %s million clusters on the lane. %s\%% of these had both reads align to the reference genome.' % (numclusters, pctalign)))
            doc.append(NewPage())
        elif pdfimg.endswith('_capture_specificity.pdf'):
            doc.append(NoEscape(r'\section{Capture Specificity}'))
            go_to_toc(doc)
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg,width=scalewidth)
                pctonnearbait = str(projdf['SummaryValue'][3])
                pctonbait = str(projdf['SummaryValue'][4])
                pctontarget = str(projdf['SummaryValue'][5])
                qc_fig.add_caption(NoEscape(r'Capture Specificity: Average \%% selected on/near bait = %s\%%. Average \%% on bait = %s\%%.' % (pctonnearbait, pctonbait)))
                # qc_fig.add_caption(NoEscape(r'Capture Specificity: Average \%% selected on/near bait = %s\%%. Average \%% on bait = %s\%%. Average \%% of usable bases on target = %s\%%' % (pctonnearbait, pctonbait, pctontarget)))
            doc.append(NewPage())
        elif pdfimg.endswith('_capture_specificity_percentage.pdf'):
            doc.append(NoEscape(r'\section{Capture Specificity Relative Percentage}'))
            go_to_toc(doc)
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg,width=scalewidth)
                pctonnearbait = str(projdf['SummaryValue'][3])
                pctonbait = str(projdf['SummaryValue'][4])
                pctontarget = str(projdf['SummaryValue'][5])
                qc_fig.add_caption(NoEscape(r'Capture Specificity: Average \%% selected on/near bait = %s\%%. Average \%% on bait = %s\%%.' % (pctonnearbait, pctonbait)))
                # qc_fig.add_caption(NoEscape(r'Capture Specificity: Average \%% selected on/near bait = %s\%%. Average \%% on bait = %s\%%. Average \%% of usable bases on target = %s\%%' % (pctonnearbait, pctonbait, pctontarget)))
            doc.append(NewPage())
        elif pdfimg.endswith('_insert_size.pdf'):
            doc.append(NoEscape(r'\section{Insert Size Distribution}'))
            go_to_toc(doc)
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                qc_fig.add_caption('Insert Size Distribution')
            doc.append(NewPage())
        elif pdfimg.endswith('_insert_size_peaks.pdf'):
            doc.append(NoEscape(r'\section{Peak Insert Size Values}'))
            go_to_toc(doc)
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                avgpeak = str(projdf['SummaryValue'][7])
                qc_fig.add_caption(NoEscape(r'Peak Insert Size Values. Mean peak insert size = %s.' % avgpeak))
            doc.append(NewPage())
        elif pdfimg.endswith('_fingerprint.pdf'):
            doc.append(NoEscape(r'\section{Sample Mix-Ups}'))
            go_to_toc(doc)
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                qc_fig.add_caption(NoEscape(r'Sample Mixups: The value below the key refers to the fraction of discordant homozygous alleles. A low score between unrelated samples is a red flag.'))
            doc.append(NewPage())
        elif pdfimg.endswith('_major_contamination.pdf'):
            doc.append(NoEscape(r'\section{Major Contamination Check}'))
            go_to_toc(doc)
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                majcontam = str(projdf['SummaryValue'][10])
                qc_fig.add_caption(NoEscape(r'Major Contamination Check: The mean fraction of positions that are heterozygous is %s.' % majcontam))
            doc.append(NewPage())
        elif pdfimg.endswith('_minor_contamination.pdf'):
            doc.append(NoEscape(r'\section{Minor Contamination Check}'))
            go_to_toc(doc)
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                mincontam = str(projdf['SummaryValue'][11])
                qc_fig.add_caption(NoEscape(r'Minor Contamination Check: Average minor allele frequency is %s' % mincontam))
            doc.append(NewPage())
        elif pdfimg.endswith('_duplication.pdf'):
            doc.append(NoEscape(r'\section{Estimated Duplication Rate}'))
            go_to_toc(doc)
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                duprate = str(projdf['SummaryValue'][13])
                qc_fig.add_caption(NoEscape(r'Duplication Rate: Average duplication rate is %s\%%' % duprate))
            doc.append(NewPage())
        elif pdfimg.endswith('_library_size.pdf'):
            doc.append(NoEscape(r'\section{Estimated Library Size}'))
            go_to_toc(doc)
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                libsize = str(projdf['SummaryValue'][14])
                qc_fig.add_caption(NoEscape(r'Estimated Library Size: Average library size is %s million' % libsize))
            doc.append(NewPage())
        elif pdfimg.endswith('_coverage.pdf'):
            doc.append(NoEscape(r'\section{Mean Target Coverage}'))
            go_to_toc(doc)
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                cover = str(projdf['SummaryValue'][15])
                qc_fig.add_caption(NoEscape(r'Median Target Coverage: Median canonical exon coverage across all samples is %sx' % cover))
            doc.append(NewPage())
        elif pdfimg.endswith('_trimmed_reads.pdf'):
            doc.append(NoEscape(r'\section{Percentage of Reads Trimmed}'))
            go_to_toc(doc)
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                qc_fig.add_caption(NoEscape(r'Percent trimmed reads'))
            doc.append(NewPage())
        elif pdfimg.endswith('_base_qualities.pdf'):
            doc.append(NoEscape(r'\section{Pre \& Post-Recalibration Quality Scores}'))
            go_to_toc(doc)
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                qc_fig.add_caption(NoEscape(r'Base Qualities'))
            doc.append(NewPage())
        elif pdfimg.endswith('_gc_bias.pdf'):
            doc.append(NoEscape(r'\section{Normalized Coverage vs GC-Content}'))
            go_to_toc(doc)
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                qc_fig.add_caption(NoEscape(r'GC Content'))
            doc.append(NewPage())
        elif pdfimg.endswith('_hotspots.pdf'):
            doc.append(NoEscape(r'\section{HOTSPOTS in NORMALS}'))
            go_to_toc(doc)
            # doc.append(NoEscape(r'\includepdf[pages={1-},scale=0.75]{Proj_06208_C_hotspots.pdf}'))
            for i in range(count_pages(pdfimg)):
                i = i+1
                with doc.create(Figure(position='h!')) as qc_fig:
                    qc_fig.add_image(pdfimg, width=smallscalewidth, page=i)
                    # qc_fig.add_caption(NoEscape(r'hotspots caption'))
                doc.append(NewPage())
        elif pdfimg.endswith('_cdna_contamination.txt'):
            doc.append(NoEscape(r'\section{cDNA contamination check}'))
            go_to_toc(doc)
            cdnadf = pd.read_csv(pdfimg, sep='\t')
            # cdnadf = cdnadf.replace(pd.np.nan, '', regex=True)
            with doc.create(LongTabu("|X[c]|X[c]|X[c]|", row_height=1.5)) as data_table:
                # with doc.create(LongTabu(r"|c|l|l|l|X[c]|X[c]|X[c]|X[c]|m{1cm}|>{\raggedright}m{1cm}|m{1cm}|X[c]|m{1cm}|", row_height=2.5)) as data_table:
                    header_row1 = ["Sample","Hugo_Symbol","Count"]
                    data_table.add_hline()
                    data_table.add_row(header_row1, mapper=bold)
                    data_table.add_hline()
                    data_table.end_table_header()
                    data_table.add_hline()
                    data_table.end_table_last_footer()
                    for index, row in cdnadf.iterrows():
                        prow = row.tolist()
                        data_table.add_row(prow[0], prow[1], prow[2])
                        data_table.add_hline()
            doc.append(NewPage())
        elif pdfimg.endswith('_concordance.pdf'):
            doc.append(NoEscape(r'\section{Conpair Concordance}'))
            go_to_toc(doc)
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=small_scalewidth)
                # qc_fig.add_caption(NoEscape(r'GC Content'))
            doc.append(NewPage())
        else:
            print('Other files found, but ignoring: ',pdfimg)
            # doc.append(NoEscape(r'\section{AWESOME FIGURE}'))
            # go_to_toc(doc)
            # with doc.create(Figure(position='h!')) as qc_fig:
            #     qc_fig.add_image(pdfimg,width=scalewidth)
            #     qc_fig.add_caption('Look it\'s on its back')
            # doc.append(NewPage())
    doc.generate_pdf(args.full_project_name+'_QC_Report', clean_tex=True)#, compiler='latexmk -interaction=nonstopmode')
