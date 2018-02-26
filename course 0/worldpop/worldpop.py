import collections
population_2010_dict = collections.defaultdict(int)
population_2100_dict = collections.defaultdict(int)
population_growth = collections.defaultdict(int)
area_dict = collections.defaultdict(int)
density_dict = collections.defaultdict(int)

with open('lecz-urban-rural-population-land-area-estimates-v2-csv/lecz-urban-rural-population-land-area-estimates_continent-90m.csv','rU') as inputFile:
    header = next(inputFile)
    for line in inputFile:
        line = line.rstrip().split(',')
        line[5] = int(line[5])
        line[6] = int(line[6])
        line[7] = int(line[7])
        if line[1] == 'Total National Population':
            population_2010_dict[line[0]] += line[5]
            population_2100_dict[line[0]] += line[6]
            area_dict[line[0]] += line[7]
for j in range(len(population_2010_dict.keys())):
	population_growth.update({population_2010_dict.keys()[j]:float(population_2100_dict[population_2010_dict.keys()[j]]-population_2010_dict[population_2010_dict.keys()[j]])/population_2010_dict[population_2010_dict.keys()[j]]})
	density_dict.update({population_2010_dict.keys()[j]:float(population_2010_dict[population_2010_dict.keys()[j]]/area_dict[population_2010_dict.keys()[j]])})

with open('national_population_analysis.csv', 'w') as outputFile:
    outputFile.write('continent,population_growth,density\n')

    for k, x, v in zip(population_2010_dict.keys(), population_growth.values(), density_dict.values()):
        outputFile.write(k + ',' + str(x) + ',' + str(v) + '\n')