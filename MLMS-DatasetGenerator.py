import DataExtractor as de
import sys
import csv

if (len(sys.argv) != 6):
    print(len(sys.argv))
    print('Argument error')
    input()
    exit(1)

args = {
    'boardWidth' : int(sys.argv[1]),
    'boardHeight' : int(sys.argv[2]),
    'boardMineCount' : int(sys.argv[3]),
    'testRadius' : int(sys.argv[4]),
    'testCount' : int(sys.argv[5]),
}

output = {
    'labels' : [],
    'data' : []
}

output['labels'] = de.getCellLabels(args['testRadius'])

testTotal = 0
while (testTotal < args['testCount']):

    testGame = de.boardTest(args['boardWidth'],args['boardHeight'],args['boardMineCount'])
    testBoard = testGame.board

    zeroCells = de.getZeroCells(testBoard.data)
    bordCells = de.getBorderCells(testBoard.data, zeroCells)
    testCells = de.getBorderBorders(bordCells, testBoard.data)

    for ix, x, in enumerate(testCells):
        if not(testTotal < args['testCount']):
                break
        for iy, y in enumerate(x):
            if not(testTotal < args['testCount']):
                break
            if (y == 1):
                
                output['data'].append(de.getMLinput(testGame.maskd,ix,iy,args['testRadius']))
                testTotal = testTotal + 1

#Json saver
#outputFileName = 'dataset_{}x{}-{}m_{}t-{}r.json'.format(*list(args.values()))

#with open(outputFileName, "w") as outfile:
    #json.dump(output, outfile)

#CSV saver
outputFileName = 'dataset_{}x{}-{}m_{}r-{}t.csv'.format(*list(args.values()))    

with open(outputFileName, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    writer.writerow(output['labels'])

    for d in output['data'] :
        writer.writerow(d)

print('{} has successfully been saved'.format(outputFileName))
input()


