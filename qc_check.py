import sys,subprocess,glob

def tranpose_file(f,temp_file_name):
    cmd = "./transpose.sh " + f + " > " + temp_file_name
    return subprocess.call(cmd, shell=True)

def delete_tmp_file(filename):
    cmd = "rm " + filename
    return subprocess.call(cmd, shell=True)


def read_pairing_file(f):
    #returns d[tumor_sample_id]=normal_sample_id
    d={}
    with open(f) as pairing_file:
        for line in pairing_file:
            normal_sample_id,tumor_sample_id=line.rstrip().split()
            if tumor_sample_id in d:
                print 'Error: one tumor paired with multiple normals'
            d[tumor_sample_id]=normal_sample_id
    return d

def read_sample_data_clinical_file(f):
    #d={sample{Collab_ID=...,Sample_ID=...},sample2{}}
    d={} #rowId -> Collab_ID
    d2={}#patient id -> list of rowids
    with open(f) as sample_data_clinical_file:
        sample_data_clinical_file.readline() #skip headerline
        for line in sample_data_clinical_file:
            line=line.rstrip().split()
            Sample_ID =line[0]
            Patient_ID=line[3]
            Collab_ID =line[4]
            if Sample_ID in d:
                print 'error:Duplicate Sample_ID'
                sys.exit(1)
            d[Sample_ID]=Collab_ID
            if Patient_ID not in d2:
                d2[Patient_ID]=[]
            d2[Patient_ID].append(Sample_ID)
    return {'rowId':d, 'patient_id_list':d2}


def check_homo_concordance(clinical_data_dict,homo_concordance_file,pairing_file,match_threshold):
    print 'Checking homo_concordance'

    temp_file_name='tmp'
    output=tranpose_file(homo_concordance_file,temp_file_name)

    if output:
        print "error: couldn't transpose the file"
        sys.exit(1)

    input_file=temp_file_name

    pair_ids_d=read_pairing_file(pairing_file)

    with open(input_file,'r') as input_qc_file:

        headerline=input_qc_file.readline().split()
        col_ids=headerline[1:]

        for line in input_qc_file:
            line=line.rstrip().split()
            row_id=line[0]
            collab_id=clinical_data_dict['rowId'][row_id]

            pair_id=pair_ids_d[row_id]
            pair_collab_id=clinical_data_dict['rowId'][pair_id]

            same_patient_different_ids=clinical_data_dict['patient_id_list']


            values=[float(item) for item in line[1:]]
            passed_threshold=[i for i,j in enumerate(values) if j >= match_threshold]

            # if pair_id=='s_FROZENPOOLEDNORMAL':
            #     continue

            #didn't match anything, including its pair
            if len(passed_threshold)==0:
                print row_id+' ('+collab_id+") didn't match any genotype, including its pair "+pair_id+' ('+pair_collab_id+')'

            matched_col_ids=[col_ids[item] for item in passed_threshold]

            #didn't match its pair, but matched a different sample
            if len(passed_threshold)==1 and matched_col_ids[0] != pair_id :
                print row_id+'('+collab_id+") didn't match its pair ("+pair_id+"), instead matched a different sample"+matched_col_ids[0]+' ('+clinical_data_dict['rowId'][matched_col_ids[0]]+')'
            if len(passed_threshold)==1 and matched_col_ids[0] != pair_id and matched_col_ids[0] in same_patient_different_ids :
                print row_id,'(',collab_id+") didn't match its pair ("+pair_id+"), instead matched a different sample from same patient"+matched_col_ids[0]+' ('+clinical_data_dict['rowId'][matched_col_ids[0]]+')'

            #matched multiple genotypes
            if len(passed_threshold)>1:
                if pair_id not in matched_col_ids:
                    print row_id+'(',clinical_data_dict['rowId'][row_id]+") didn't match its pair, but matched other ids"+matched_col_ids
                else:
                    print row_id+'(',clinical_data_dict['rowId'][row_id]+") matched its pair, but also matched other ids"+matched_col_ids

    output=delete_tmp_file('tmp')
    if output:
        print "error: couldn't delete the temp file"
        sys.exit(1)

def check_cdna_contamination(clinical_data_dict,cdna_contamination_file):
    print 'Checking cDNA contamination'
    f=open(cdna_contamination_file)
    if 'No detected cDNA contamination' in f.readline():
        print 'All good'
        return 0
    d={} #d[sample_id]=[list of genes]
    for line in f:
        tumor_sample_barcode,hugo_symbol,count=line.rstrip().split()
        if tumor_sample_barcode not in d:
            d[tumor_sample_barcode]=[]
        d[tumor_sample_barcode].append(hugo_symbol)

    for item in d:
        print item+' ('+clinical_data_dict['rowId'][item]+') has cDNA contamination of genes '+','.join(d[item])


    return 0




def main():

    match_threshold=70

    project_path=sys.argv[1]

    homo_concordance_file    =glob.glob(project_path+'/qc_metrics/consolidated_metrics/*_homo_concordance.txt')[0] #qc/..._homo_concordance.txt
    cdna_contamination_file  =glob.glob(project_path+'/qc_metrics/consolidated_metrics/*_cdna_contamination.txt')[0] #qc/..._cdna_contamination.txt
    pairing_file             =glob.glob(project_path+'/sample_pairing.txt')[0] #inputs/..._sample_pairing.txt
    sample_data_clinical_file=glob.glob(project_path+'/sample_data_clinical.txt')[0] #sample_data_clinical.txt

    clinical_d=read_sample_data_clinical_file(sample_data_clinical_file)
    check_homo_concordance(clinical_d,homo_concordance_file,pairing_file,match_threshold)
    check_cdna_contamination(clinical_d,cdna_contamination_file)

if __name__ == '__main__':
    main()
