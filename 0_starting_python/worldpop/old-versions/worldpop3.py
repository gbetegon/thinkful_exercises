import collections
population_dict = collections.defaultdict(int)

with open('lecz-urban-rural-population-land-area-estimates-v2-csv/lecz-urban-rural-population-land-area-estimates_continent-90m.csv','rU') as inputFile:
    header = next(inputFile)

    for line in inputFile:
        line = line.rstrip().split(',')
        line[5] = int(line[5])
        line[6] = int(line[6])
        x = (line[6] - line [5])/line[5]
        if line[1] == 'Total National Population':
            population_dict[line[0]] += x

with open('national_population_increase3.csv', 'w') as outputFile:
    outputFile.write('continent,population increase\n')

    for k, v, in population_dict.iteritems():
        outputFile.write(k + ',' + str(v) + '\n')