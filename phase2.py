import os

def reset():
    cmnd = "rm -f r_sorted.txt t_sorted.txt y_sorted.txt \
    r.txt t.txt y.txt re.idx te.idx ye.idx"
    os.system(cmnd)

def phase_two():
    # get rid of old files
    reset()

    # commands will be stored here
    commands = []

    # series of commands for phase 2
    sort_r = "sort -u recs.txt >  r_sorted.txt"
    sort_t = "sort -u terms.txt >  t_sorted.txt"
    sort_y = "sort -u years.txt >  y_sorted.txt"
    format_r = "perl break.pl <r_sorted.txt> r.txt"
    format_t = "perl break.pl <t_sorted.txt> t.txt"
    format_y = "perl break.pl <y_sorted.txt> y.txt"
    hash_r = "< r.txt db_load -T -c duplicates=1 -t hash re.idx"
    btree_t = "< t.txt db_load -T -c duplicates=1 -t btree te.idx"
    btree_y = "< y.txt db_load -T -c duplicates=1 -t btree ye.idx"

    # add commands to the list
    commands.extend((sort_r,sort_t,sort_y,format_r, format_t, format_y,\
        hash_r, btree_t, btree_y))

    # run commands in terminal
    for cmnd in commands:
        os.system(cmnd)

    # to see the results, run:
    # db_dump -p indexname.idx

    return True

def main():
    phase_two()

    print("\nPhase 1 complete!\n")

    return True

main()