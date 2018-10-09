from pylatex import Document, Section, Command, Figure, NewPage, Tabular, LongTabu, MultiColumn, MultiRow, Table
from pylatex.package import Package
from pylatex.utils import NoEscape, bold, escape_latex
import glob,os
import pandas as pd

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

if __name__ == '__main__':
    projfile = 'files/Proj_06208_G_ProjectSummary.txt'
    samplefile = 'files/Proj_06208_G_SampleSummary.txt'
    proj = escape_latex(r'Proj_06208_G')
    geometry_options = {"tmargin": "1cm", "bmargin": "2cm", "lmargin": "1cm", "rmargin": "1cm"}
    doc = Document(geometry_options=geometry_options)
    doc.documentclass = Command(
        'documentclass',
        options=['10pt', 'landscape'],
        lmodern=False,
        arguments=['article'],
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
    doc.packages.append(Package('tgheros'))
    doc.packages.append(Package('caption'))
    doc.append(NoEscape(r'\captionsetup{labelsep=period}'))



    doc.append(NoEscape(r'\begin{titlepage}'))
    doc.append(NoEscape(r'\begin{center}'))
    doc.append(NoEscape(r'\vspace{1cm}'))
    doc.append(NoEscape(r'\Large'))
    doc.append(NoEscape(r'\textbf{Memorial Sloan Kettering Cancer Center Center for Molecular Oncology}\\'))

    doc.append(NoEscape(r'\vspace{5.5cm}'))
    doc.append(NoEscape(r'\LARGE'))
    doc.append(NoEscape(r'\textbf{Project %s}\\' % proj))
    doc.append(NoEscape(r'\textbf{QC Metrics Report}\\'))
    doc.append(NoEscape(r'\vspace{1.5cm}'))
    # doc.append(NoEscape(r'\textbf{Author Name}\\'))
    doc.append(NoEscape(r'\vfill'))
    doc.append(NoEscape(r'\end{center}'))
    doc.append(NoEscape(r'\end{titlepage}'))



 
    #    \vfill
 
    #    A thesis presented for the degree of\\
    #    Doctor of Philosophy
 
    #    \vspace{0.8cm}
 
    #    \includegraphics[width=0.4\textwidth]{university}
 
    #    Department Name\\
    #    University Name\\
    #    Country\\
    #    Date

    doc.append(NewPage())

    doc.append(NoEscape(r'\footnotesize'))
    projdf = pd.read_csv(projfile, sep='\t')
    projdf = projdf.replace(pd.np.nan,'',regex=True)

    sampdf = pd.read_csv(samplefile, sep='\t')
    sampdf = sampdf.replace(pd.np.nan, '', regex=True)
    with doc.create(LongTabu("|c|l|c|X[p]|c|X[m]|", row_height=1.5)) as data_table:
        header_row1 = ["AutoStatus", "Metric", "Category", "Summary Description", "Summary Value", "Failures"]
        data_table.add_hline()
        data_table.add_row(header_row1,mapper=bold)
        data_table.add_hline()

        for index, row in projdf.iterrows():
            # if row['Metric'] == 'Cluster Density':
            if index == 0: ## Cluster Density
                prow = row.tolist()
                data_table.add_row((MultiRow(2,data=colorcellStatus(row['AutoStatus'],'color')),MultiRow(2,data=row['Metric']),prow[2],prow[3],prow[4],prow[5] ))
                data_table.add_hline(3,6)
            elif index == 1:
                prow = row.tolist()
                data_table.add_row((MultiRow(NoEscape(-2),data=colorcellStatus(row['AutoStatus'],'text')),MultiRow(2,data=''),prow[2],prow[3],prow[4],prow[5] ))
                data_table.add_hline()
            elif index == 3: ## Capture Specificity (skipping index 2 because its formatted weird..)
                prow = row.tolist()
                data_table.add_row((MultiRow(3, data=colorcellStatus(row['AutoStatus'], 'color')), MultiRow(3, data=row['Metric']), MultiRow(3, data=''), prow[3], prow[4], prow[5]))
                data_table.add_hline(4,6)
            elif index == 4:
                prow = row.tolist()
                data_table.add_row((MultiRow(3, data=colorcellStatus(row['AutoStatus'], 'color')), MultiRow(3, data=''), MultiRow(3, data=''), prow[3], prow[4], prow[5]))
                data_table.add_hline(4, 6)
            elif index == 5:
                prow = row.tolist()
                data_table.add_row((MultiRow(NoEscape(-3), data=colorcellStatus(row['AutoStatus'], 'text')), MultiRow(3, data=''), MultiRow(3, data=''), prow[3], prow[4], prow[5]))
                data_table.add_hline()
            elif index == 7: #Insert Size, index 6 not used?!
                prow = row.tolist()
                data_table.add_row(colorcellStatus(prow[0],'text'), prow[1], prow[2], prow[3],prow[4],prow[5])
                data_table.add_hline()
            elif index == 8: # Sample Labeling Errors
                prow = row.tolist()
                data_table.add_row((MultiRow(2, data=colorcellStatus(row['AutoStatus'],'color')), MultiRow(2, data=NoEscape(row['Metric']),width='2.5cm'), prow[2], prow[3], prow[4], prow[5]))
                data_table.add_hline(3, 6)
            elif index == 9:
                prow = row.tolist()
                data_table.add_row((MultiRow(NoEscape(-2), data=colorcellStatus(row['AutoStatus'],'text')), MultiRow(2, data=''), prow[2], prow[3], prow[4], prow[5]))
                data_table.add_hline()
            elif index == 10: # Contamination
                prow = row.tolist()
                # data_table.add_row((MultiRow(2, data=row['AutoStatus']), MultiRow(2, data=NoEscape(r'{\parbox{10cm}{'+row['Metric']+'}}')), prow[2], prow[3], prow[4], prow[5]))
                data_table.add_row((MultiRow(3, data=colorcellStatus(row['AutoStatus'], 'color')), MultiRow(3, data=NoEscape(row['Metric'])), prow[2], prow[3], prow[4], prow[5]))
                data_table.add_hline(3, 6)
            elif index == 11:
                prow = row.tolist()
                data_table.add_row((MultiRow(3, data=colorcellStatus(row['AutoStatus'], 'color')), MultiRow(3, data=''), prow[2], prow[3], prow[4], prow[5]))
                data_table.add_hline(3,6)
            elif index == 12:
                prow = row.tolist()
                data_table.add_row((MultiRow(NoEscape(-3), data=colorcellStatus(prow[0], 'text')), MultiRow(3, data=''), prow[2], prow[3], prow[4], prow[5]))
                data_table.add_hline()
            elif index == 13: #Duplication
                prow = row.tolist()
                data_table.add_row(colorcellStatus(prow[0], 'text'), prow[1], prow[2], prow[3], prow[4], prow[5])
                data_table.add_hline()
            elif index == 14: #Library Size
                prow = row.tolist()
                data_table.add_row(colorcellStatus(prow[0], 'text'), prow[1], prow[2], prow[3], prow[4], prow[5])
                data_table.add_hline()
            elif index == 15:  # Target Coverage
                prow = row.tolist()
                data_table.add_row((MultiRow(3, data=colorcellStatus(row['AutoStatus'], 'color')), MultiRow(3, data=NoEscape(row['Metric'])), prow[2], prow[3], prow[4], prow[5]))
                data_table.add_hline(3, 6)
            elif index == 16:
                prow = row.tolist()
                data_table.add_row((MultiRow(3, data=colorcellStatus(row['AutoStatus'], 'color')), MultiRow(3, data=''), prow[2], prow[3], prow[4], prow[5]))
                data_table.add_hline(3, 6)
            elif index == 17:
                prow = row.tolist()
                data_table.add_row((MultiRow(NoEscape(-3), data=colorcellStatus(prow[0], 'text')), MultiRow(3, data=''), prow[2], prow[3], prow[4], prow[5]))
                data_table.add_hline()

    doc.append(NewPage())

    # with doc.create(LongTabu("|X[c]|X[c]|X[p]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|X[c]|", row_height=1.5)) as data_table:
    with doc.create(LongTabu(r"|c|l|l|l|X[c]|X[c]|X[c]|X[c]|m{1cm}|>{\raggedright}m{1cm}|m{1cm}|X[c]|m{1cm}|", row_height=2.5)) as data_table:
        header_row1 = ["Status","Sample","Unexpected Match","Unexpected Mismatch","Major Contam.","Minor Contam.","Coverage","Duplication","Library Size (millions)","On Bait Bases (millions)","Aligned Reads (millions)","Insert Size Peak","% Trimmed Reads"]
        data_table.add_hline()
        # doc.append(NoEscape(r'\rowfont{\tiny}'))
        data_table.add_row(header_row1, mapper=bold)
        data_table.add_hline()

        for index, row in sampdf.iterrows():
            # if row['Metric'] == 'Cluster Density':
            # if index == 0:  # Cluster Density
            if index == 0:
                prow = row.tolist()
                # data_table.add_row(prow)
                data_table.add_row((MultiRow(1, data=prow[0]), prow[1], prow[2], prow[3], prow[4], prow[5], prow[6], prow[7], prow[8], prow[9], prow[10], prow[11], prow[12]))
                data_table.add_hline()
            else:
                prow = row.tolist()
                # data_table.add_row(prow)
                data_table.add_row((MultiRow(1, data=colorcellStatus(prow[0], 'text')), prow[1], prow[2], prow[3], prow[4], prow[5], prow[6], prow[7], prow[8], prow[9], prow[10], prow[11], prow[12]))
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

    doc.append(NoEscape(r'\large'))
    doc.append(NoEscape(r'\hypertarget{toc}{}'))
    doc.append(NoEscape(r'\tableofcontents'))
    doc.append(NewPage())
    
    doc.append(NoEscape(r'\normalsize'))
    path = 'images'
    #this will be tied to qc_summary.R
    scalewidth = NoEscape(r'.91\textwidth')
    for pdfimg in glob.glob(os.path.join(path, '*.pdf')):
        if pdfimg.endswith('_alignment.pdf'):
            doc.append(NoEscape(r'\section{Cluster Density \& Alignment Rate}'))
            doc.append(NoEscape(r'Go to \hyperlink{toc}{TOC}'))
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                numclusters = str(int(projdf['SummaryValue'][0]))
                pctalign = str(projdf['SummaryValue'][1]*100)
                qc_fig.add_caption(NoEscape(r'Cluster Density: There were a total of %s million lusters on the lane. %s\%% of these had both reads align to the reference genome.' % (numclusters,pctalign)))
            doc.append(NewPage())
        elif pdfimg.endswith('_alignment_percentage.pdf'):
            doc.append(NoEscape(r'\section{Cluster Density \& Alignment Rate}'))
            doc.append(NoEscape(r'Go to \hyperlink{toc}{TOC}'))
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                numclusters = str(int(projdf['SummaryValue'][0]))
                pctalign = str(projdf['SummaryValue'][1]*100)
                qc_fig.add_caption(NoEscape(r'Cluster Density: There were a total of %s million lusters on the lane. %s\%% of these had both reads align to the reference genome.' % (numclusters, pctalign)))
            doc.append(NewPage())
        elif pdfimg.endswith('_capture_specificity.pdf'):
            doc.append(NoEscape(r'\section{Capture Specificity}'))
            doc.append(NoEscape('Go to \hyperlink{toc}{TOC}'))
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg,width=scalewidth)
                pctonnearbait = str(projdf['SummaryValue'][3])
                pctonbait = str(projdf['SummaryValue'][4])
                pctontarget = str(projdf['SummaryValue'][5])
                qc_fig.add_caption(NoEscape(r'Capture Specificity: Average \%% selected on/near bait = %s\%%. Average \%% on bait = %s\%%. Average \%% of usable bases on target = %s\%%' % (pctonnearbait, pctonbait, pctontarget)))
            doc.append(NewPage())
        elif pdfimg.endswith('_capture_specificity_percentage.pdf'):
            doc.append(NoEscape(r'\section{Capture Specificity}'))
            doc.append(NoEscape('Go to \hyperlink{toc}{TOC}'))
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg,width=scalewidth)
                pctonnearbait = str(projdf['SummaryValue'][3])
                pctonbait = str(projdf['SummaryValue'][4])
                pctontarget = str(projdf['SummaryValue'][5])
                qc_fig.add_caption(NoEscape(r'Capture Specificity: Average \%% selected on/near bait = %s\%%. Average \%% on bait = %s\%%. Average \%% of usable bases on target = %s\%%' % (pctonnearbait, pctonbait, pctontarget)))
            doc.append(NewPage())
        elif pdfimg.endswith('_insert_size.pdf'):
            doc.append(NoEscape(r'\section{Insert Size Distribution}'))
            doc.append(NoEscape('Go to \hyperlink{toc}{TOC}'))
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                qc_fig.add_caption('Insert Size Distribution')
            doc.append(NewPage())
        elif pdfimg.endswith('_insert_size_peaks.pdf'):
            doc.append(NoEscape(r'\section{Peak Insert Size Values}'))
            doc.append(NoEscape('Go to \hyperlink{toc}{TOC}'))
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                avgpeak = str(projdf['SummaryValue'][7])
                qc_fig.add_caption(NoEscape(r'Peak Insert Size Values. Mean peak insert size = %s.' % avgpeak))
            doc.append(NewPage())
        elif pdfimg.endswith('_fingerprint.pdf'):
            doc.append(NoEscape(r'\section{Sample Mix-Ups}'))
            doc.append(NoEscape('Go to \hyperlink{toc}{TOC}'))
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                qc_fig.add_caption(NoEscape(r'Sample Mixups: The value below the key refers to the fraction of discordant homozygous alleles. A low score between unrelated samples is a red flag.'))
            doc.append(NewPage())
        elif pdfimg.endswith('_major_contamination.pdf'):
            doc.append(NoEscape(r'\section{Major Contamination Check}'))
            doc.append(NoEscape('Go to \hyperlink{toc}{TOC}'))
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                majcontam = str(projdf['SummaryValue'][10])
                qc_fig.add_caption(NoEscape(r'Major Contamination Check: The mean fraction of positions that are heterozygous is %s.' % majcontam))
            doc.append(NewPage())
        elif pdfimg.endswith('_minor_contamination.pdf'):
            doc.append(NoEscape(r'\section{Minor Contamination Check}'))
            doc.append(NoEscape('Go to \hyperlink{toc}{TOC}'))
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                mincontam = str(projdf['SummaryValue'][11])
                qc_fig.add_caption(NoEscape(r'Minor Contamination Check: Average minor allele frequency is %s' % mincontam))
            doc.append(NewPage())
        elif pdfimg.endswith('_duplication.pdf'):
            doc.append(NoEscape(r'\section{Estimated Duplication Rate}'))
            doc.append(NoEscape('Go to \hyperlink{toc}{TOC}'))
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                duprate = str(projdf['SummaryValue'][13])
                qc_fig.add_caption(NoEscape(r'Duplication Rate: Average duplication rate is %s\%%' % duprate))
            doc.append(NewPage())
        elif pdfimg.endswith('_library_size.pdf'):
            doc.append(NoEscape(r'\section{Estimated Library Size}'))
            doc.append(NoEscape('Go to \hyperlink{toc}{TOC}'))
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                libsize = str(projdf['SummaryValue'][14])
                qc_fig.add_caption(NoEscape(r'Estimated Library Size: Average library size is %s million' % libsize))
            doc.append(NewPage())
        elif pdfimg.endswith('_coverage.pdf'):
            doc.append(NoEscape(r'\section{Mean Target Coverage}'))
            doc.append(NoEscape('Go to \hyperlink{toc}{TOC}'))
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                cover = str(projdf['SummaryValue'][15])
                qc_fig.add_caption(NoEscape(r'Median Target Coverage: Median canonical exon coverage across all samples is %sx' % cover))
            doc.append(NewPage())
        elif pdfimg.endswith('_trimmed_reads.pdf'):
            doc.append(NoEscape(r'\section{Percentage of Reads Trimmed}'))
            doc.append(NoEscape('Go to \hyperlink{toc}{TOC}'))
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                qc_fig.add_caption(NoEscape(r'Percent trimmed reads'))
            doc.append(NewPage())
        elif pdfimg.endswith('_base_qualities.pdf'):
            doc.append(NoEscape(r'\section{Pre \& Post-Recalibration Quality Scores}'))
            doc.append(NoEscape('Go to \hyperlink{toc}{TOC}'))
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                qc_fig.add_caption(NoEscape(r'Base Qualities'))
            doc.append(NewPage())
        elif pdfimg.endswith('_gc_bias.pdf'):
            doc.append(NoEscape(r'\section{Normalized Coverage vs GC-Content}'))
            doc.append(NoEscape('Go to \hyperlink{toc}{TOC}'))
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg, width=scalewidth)
                qc_fig.add_caption(NoEscape(r'GC Content'))
            doc.append(NewPage())
        else:
            doc.append(NoEscape(r'\section{AWESOME FIGURE}'))
            doc.append(NoEscape('Go to \hyperlink{toc}{TOC}'))
            with doc.create(Figure(position='h!')) as qc_fig:
                qc_fig.add_image(pdfimg,width=scalewidth)
                qc_fig.add_caption('Look it\'s on its back')
            doc.append(NewPage())
    doc.generate_pdf('test', clean_tex=False)



#
