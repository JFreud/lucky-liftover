import os


def write_line(oline_toks, lline_toks, new_obj):
    if oline_toks[1] == lline_toks[3]: #if rsids match
        oline_toks[3] = lline_toks[2] #set to lifted position
        new_obj.write("\t".join(oline_toks) + "\n")
        return True
    else:
        oline_toks[3] = str(-1)
        new_obj.write("\t".join(oline_toks) + "\n")
        return False


def compile_new_bim(ucsc_bed, old_bim):
    with open(old_bim, "r") as oldbim, open(ucsc_bed, "r") as lifted, open("AGoateDataGSA_unimputed_hg19.bim", "w+") as newbim:
        increment_lifted = True
        for line in oldbim:
            oline_toks = line.split()
            if (increment_lifted):
                lline_toks = lifted.readline().split()
                increment_lifted = write_line(oline_toks, lline_toks, newbim)
            else:
                increment_lifted = write_line(oline_toks, lline_toks, newbim)


if __name__ == "__main__":
    cmd = "awk '{print \"chr\"$1, $4-1, $4, $2}' AGoateDataGSA_unimputed_renamed.bim > AGoateDataGSA_unimputed.ucsc.bed"
    os.system(cmd)
    cmd = "liftOver AGoateDataGSA_unimputed.ucsc.bed hg38ToHg19.over.chain.gz AGoateDataGSA_unimputed_hg19.ucsc.bed unlifted.bed"
    os.system(cmd)
    compile_new_bim("AGoateDataGSA_unimputed_hg19.ucsc.bed", "AGoateDataGSA_unimputed_renamed.bim")
    cmd = "rm AGoateDataGSA_unimputed.ucsc.bed AGoateDataGSA_unimputed_hg19.ucsc.bed unlifted.bed"
    os.system(cmd)
