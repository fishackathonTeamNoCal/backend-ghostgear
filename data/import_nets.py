import csv
import sys
import json

class PdfParser(object):
    def parseFile(self, inputFile):
        try:
            with open(inputFile) as pdffile:
                pdfreader = csv.reader(pdffile, delimiter=':')
                nets_results = []

                net_code = None
                data = {}
                for row in pdfreader:
                    if len(row) == 0:
                        continue

                    if 'NET CODE' in row[0]:
                        if net_code is not None:
                            nets_results.append(data)
                        net_code = row[1].replace(',', '')
                        data = {'netCode':row[1].replace(',', '')}
                    else:
                        if 'COLOUR' in row[0]:
                            data['color'] = row[1].replace(',', '')
                        elif 'MESH SIZE' in row[0]:
                            if '-' in row[1]:
                                mesh_range = row[1][0:-3].split('-')
                                data['meshSize'] = float(mesh_range[0])
                            else:
                                data['meshSize'] = float(row[1][0:-3])
                        elif 'TWINE SIZE' in row[0]:
                            data['twineDiameter'] = float(row[1][0:-3])
                        elif 'STRANDS' in row[0]:
                            data['numberOfStrands'] = int(row[1].replace(',', ''))
                        elif 'ORIGIN*' in row[0]:
                            data['origin'] = row[1].replace(',', '')
                            if data['origin'] == 'Yet to be':
                                data['origin'] = 'Unknown'
                        continue
                if net_code is not None and len(data) > 1:
                    nets_results.append(data)
                print json.dumps({"results": nets_results})
        except:
            raise

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise InputError('Missing file arguments')
    #print('input' + sys.argv[1])
    PdfParser().parseFile(sys.argv[1])