import os, glob
import numpy as np
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='Input sam file')
parser.add_argument('-o', help='output folder')
parser.add_argument('--error', help='Tells the program to account for errors that can influence on the variation', action="store_true")
args = parser.parse_args()


def parse_sam_file(samfile):
    # Parses a sorted alignments SAM file for overlapping positions
    # -for each read, extracts gene it maps to, alignment position start and finish
    with open(samfile, 'r') as fid:
        all_lines = fid.readlines()

    amount = {}
    variance = {}
    inserts = {0:'fail'}
    for i in all_lines:
        line = i
        line = line.rstrip().split()
        if line[0] == '@SQ':
            ref_len = int(line[2][3:])
            for nucleotide in range(1,ref_len + 1):
                amount[nucleotide] = {'A':0, 'C':0, 'G':0, 'T':0}
            continue
        elif line[0][0] == '@':
            continue

        start_read = int(line[3])
        ins_pos = ''
        inch_pos = {}
        curr_posi = start_read
        cigar = line[5]
        if 'I' or 'D' in cigar:
            curr_posi = int(start_read)
            for i in range(len(cigar)):
                letter = cigar[i]
                try:
                    int(letter)
                    ins_pos += letter
                except ValueError:
                    if letter=='I' or letter=='D':
                        for i in range(int(ins_pos)):
                            inch_pos[curr_posi + i] = letter
                        curr_posi += int(ins_pos)
                        ins_pos = ''
                    elif letter == 'H':
                        ins_pos = ''
                    else:
                        curr_posi += int(ins_pos)
                        ins_pos = ''
        curr_nucl = start_read
        index = 0
        for j in range(len(line[9])):
            read_nucl = line[9][j]
            if inch_pos.get(curr_nucl) != None:
                if inch_pos[curr_nucl] == 'D':
                    index += 1
                    amount[curr_nucl + index][read_nucl] += 1
                else:
                    if inserts.get(curr_nucl + index) == None:
                        inserts[curr_nucl + index] = {'A':0,'C':0,'G':0,'T':0}
                    inserts[curr_nucl + index][read_nucl] += 1
                    index -= 1
            else:
                if read_nucl != 'N':
                    amount[curr_nucl + index][read_nucl] += 1
            curr_nucl += 1

    where = 0
    amount2 = {}
    for nucl in amount:
        if sum(amount[nucl].values()) == 0:
            variance[nucl+where] = None
        else:
            if inserts.get(nucl) != None:
                variance[nucl+where] = 1.0 - max(amount[nucl].values())/float(sum(amount[nucl].values()))
                amount2[nucl+where] = amount[nucl]
                amount2[nucl+where]['-'] = 0
                where += 1
                variance[nucl+where] = 1.0 - (float(sum(amount[nucl].values())) - sum(inserts[nucl].values()))/float(sum(amount[nucl].values()))
                amount2[nucl+where] = inserts[nucl]
                amount2[nucl+where]['-'] = int(float(sum(amount[nucl].values())) - sum(inserts[nucl].values()))
            else:
                variance[nucl+where] = 1.0 - max(amount[nucl].values())/float(sum(amount[nucl].values()))
                amount2[nucl+where] = amount[nucl]
                amount2[nucl+where]['-'] = 0
    return variance, amount2


def parse_sam_file_error(samfile):
    # Parses a sorted alignments SAM file for overlapping positions
    # -for each read, extracts gene it maps to, alignment position start and finish
    with open(samfile, 'r') as fid:
        all_lines = fid.readlines()

    amount = {}
    variance = {}
    inserts = {0:'fail'}
    for i in all_lines:
        line = i
        line = line.rstrip().split()
        if line[0] == '@SQ':
            ref_len = int(line[2][3:])
            for nucleotide in range(1,ref_len + 1):
                amount[nucleotide] = {'A':0, 'C':0, 'G':0, 'T':0}
            continue
        elif line[0][0] == '@':
            continue

        start_read = int(line[3])
        ins_pos = ''
        inch_pos = {}
        curr_posi = start_read
        cigar = line[5]
        if 'I' or 'D' in cigar:
            curr_posi = int(start_read)
            for i in range(len(cigar)):
                letter = cigar[i]
                try:
                    int(letter)
                    ins_pos += letter
                except ValueError:
                    if letter=='I' or letter=='D':
                        for i in range(int(ins_pos)):
                            inch_pos[curr_posi + i] = letter
                        curr_posi += int(ins_pos)
                        ins_pos = ''
                    elif letter == 'H':
                        ins_pos = ''
                    else:
                        curr_posi += int(ins_pos)
                        ins_pos = ''
        curr_nucl = start_read
        index = 0
        for j in range(len(line[9])):
            read_nucl = line[9][j]
            if inch_pos.get(curr_nucl) != None:
                if inch_pos[curr_nucl] == 'D':
                    index += 1
                    amount[curr_nucl + index][read_nucl] += 1
                else:
                    if inserts.get(curr_nucl + index) == None:
                        inserts[curr_nucl + index] = {'A':0,'C':0,'G':0,'T':0}
                    inserts[curr_nucl + index][read_nucl] += 1
                    index -= 1
            else:
                if read_nucl != 'N':
                    amount[curr_nucl + index][read_nucl] += 1
            curr_nucl += 1

    where = 0
    amount2 = {}
    for nucl in amount:
        y = 0.0
        coverage = float(sum(amount[nucl].values()))
        if coverage == 0.0:
            variance[nucl] = 0.0
        else:
            y = ((1.0/3)**((coverage**(1.0/3)) - 1.45)) + 0.05
            calc = (float(sorted(amount[nucl].values())[-2])/max(amount[nucl].values()))
            if inserts.get(nucl) != None:
                if calc>y:
                    variance[nucl+where] = 1.0 - max(amount[nucl].values())/float(coverage)
                else:
                    variance[nucl+where] = 0.0
                amount2[nucl+where] = amount[nucl]
                amount2[nucl+where]['-'] = 0
                where += 1
                variance[nucl+where] = 1.0 - (float(coverage) - sum(inserts[nucl].values()))/float(coverage)
                amount2[nucl+where] = inserts[nucl]
                amount2[nucl+where]['-'] = int(float(coverage) - sum(inserts[nucl].values()))
            else:
                if calc>y:
                    variance[nucl+where] = 1.0 - max(amount[nucl].values())/float(sum(amount[nucl].values()))
                else:
                    variance[nucl+where] = 0.0
                amount2[nucl+where] = amount[nucl]
                amount2[nucl+where]['-'] = 0
    return variance, amount2



if __name__ == "__main__":

    print("Computing SNP heterozygosities for file " + os.path.basename(args.i))
    if args.error:
        print('Take error into account')
        hz_dict, readcount_dict = parse_sam_file_error(args.i)
    else:
        hz_dict, readcount_dict  = parse_sam_file(args.i)
    if not os.path.exists(args.o):
        os.system('mkdir ' + str(args.o))
    out = ''
    out = out + 'Nucleotide,Variation,A,C,G,T,-\n'
    for j in hz_dict:
        try:
            out = out + str(j) + ',' + str(round(hz_dict[j],5)) + ',' + str(readcount_dict[j]['A']) + ',' + str(readcount_dict[j]['C']) + ',' + str(readcount_dict[j]['G']) + ',' + str(readcount_dict[j]['T']) + ',' + str(readcount_dict[j]['-']) + '\n'
        except:
            out = out + str(j) + ',0,0,0,0,0,0\n'
    name = args.i.split('/')[-1]
    print((args.o+name[:-3]+'csv'))
    output = open(args.o+name[:-3]+'csv','w')
    output.write(out)
    output.close()

