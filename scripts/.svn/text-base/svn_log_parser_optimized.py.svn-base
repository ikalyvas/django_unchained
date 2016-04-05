import fileinput,re,time


revision_pattern = re.compile(r'(r[0-9]{5,6}) \|.+\n')
block_end_pattern = re.compile(r'\-{72}\n')
start = time.clock()

a=True

for line in fileinput.input():
    revision_line = revision_pattern.match(line)
#    block_end_line = block_end_pattern.match(line)
    if revision_line:
        try:
            outfile.close()
        except NameError,e:
            print e

        outfile = open(revision_line.group(1)+'.txt','w')
    if a :
        outfile.write(line)

elapsed = (time.clock() - start)
print 'Elapsed time:' + str(elapsed)
