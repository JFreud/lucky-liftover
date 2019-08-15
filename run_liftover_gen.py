import os, sys
import argparse

def write_line(oline_toks, lline_toks, new_obj):
    if lline_toks != [] and oline_toks[1] == lline_toks[3]: #if rsids match
        oline_toks[3] = lline_toks[2] #set to lifted position
        oline_toks[0] = lline_toks[0][3:]
        new_obj.write("\t".join(oline_toks) + "\n")
        return True
    else:
        oline_toks[3] = str(-1)
        new_obj.write("\t".join(oline_toks) + "\n")
        return False


def compile_new_bim(ucsc_bed, old_bim, outfile):
    with open(old_bim, "r") as oldbim, open(ucsc_bed, "r") as lifted, open(outfile, "w+") as newbim:
        increment_lifted = True
        for line in oldbim:
            oline_toks = line.split()
            if (increment_lifted):
                lline_toks = lifted.readline().split()
                increment_lifted = write_line(oline_toks, lline_toks, newbim)
            else:
                increment_lifted = write_line(oline_toks, lline_toks, newbim)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', help='original bim file', required=True)
    parser.add_argument('-c','--chain', help='chain file for liftover', required=True)
    parser.add_argument('-o','--out', help='name of output bim file', required=True)
    parser.add_argument('-d','--debug', action='store_true', help='will not remove temp files', required=False)
    args = vars(parser.parse_args())
    inputfile = args['input']
    chainfile = args['chain']
    outfile = args['out']
    debug = args['debug']
    bedfile = "tobelifted.bed"
    cmd = "awk '$1 < 23 && $1 ~ /^[0-9]+$/ {print \"chr\"$1, $4-1, $4, $2}' " + inputfile + " > " + bedfile
    os.system(cmd)
    cmd = "liftOver " + bedfile + " " + chainfile + " lifted.bed unlifted.bed"
    os.system(cmd)
    if not os.path.isfile("lifted.bed"):
        print("Liftover did not work. Did you make sure to install ucsc's liftOver?")
        sys.exit(1)
    compile_new_bim("lifted.bed", inputfile, outfile)
    if not debug:
        cmd = "rm " + bedfile + " lifted.bed unlifted.bed"
        os.system(cmd)
    print("Liftover complete. Note: due to ucsc not being in chr 1-26 format, sex chromosomes were not lifted. SNPs that could not be lifted were assigned a position of -1, which plink will ignore.")
    print("Number of non-XY, non-alt chromosome SNPs unlifted:")
    cmd = "awk '$4==-1 && $1 > 0 && $1 < 23 && $1 ~ /^[0-9]+$/' newhg19.bim | wc -l"
    os.system(cmd)
