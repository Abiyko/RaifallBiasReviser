def sortData(revisedData):
    monthlySortedData = {}
    monthlyData = {f'{i:02d}': [] for i in range(1, 13)}

    for id, dataList in revisedData.items():
        month = id[4:6]
        monthlyData[month].extend(dataList)
    
    for month in sorted(monthlyData.keys()):
        monthDataPoints = monthlyData[month]
        
        if monthDataPoints:
            sorted_data = sorted(monthDataPoints, key=lambda x: float(x), reverse=True)
            monthlySortedData[month] = sorted_data
        else:
            print('データがありません。')
            monthlySortedData[month] = []
    
    return monthlySortedData


def calcAverage(otherRainfall, reviseFlag, currentId):
    othorIdAverages = []
    # 収集したデータの平均値を計算
    if reviseFlag == True:

        processLists = list(otherRainfall.values())
        maxLength = 0
        maxLength = max(len(l) for l in processLists)
        
        for i in range(maxLength):
            validData = []
            for rainfallList in processLists:
                # インデックスが存在し、かつデータが-9999.9でない場合にのみ追加
                if i < len(rainfallList) and rainfallList[i] != -9999.9:
                    validData.append(float(rainfallList[i]))

            if validData:
                average = sum(validData) / len(validData)
                othorIdAverages.append(average)
            else:
                print(f"{i+1}行目に有効なデータが存在しません。")
    else:
        print(f"ID {currentId} の比較対象に完全なデータがないため修正できません。")
        othorIdAverages = None
    
    return othorIdAverages


def calcDifference(otherIdAverages, currentRainfall):

    # 最も長いリストの長さに合わせてループを回す
    maxRainfallCount = 0
    maxRainfallCount = len(currentRainfall)
    
    differences = []
    
    for i in range(maxRainfallCount):

        currentRainfall[i] = float(currentRainfall[i])
        if currentRainfall[i] == -9999.9:
            difference = 0
        else:
            difference = otherIdAverages[i] - currentRainfall[i]
            if difference < 0:
                difference = 0
        
        differences.append((difference, otherIdAverages[i]))
    
    sortedDifferences = sorted(differences, key=lambda x: x[0], reverse = True)
    return sortedDifferences


def formatLines(lines):
    formattedLines = []
    idData = {}

    for line in lines:

        # コメント行または空の行、カンマが含まれていない行をスキップ
        if line.startswith('#') or not line:
            continue
        
        # 分割されたリストの要素数が2未満の場合スキップ
        parts = line.split(',')
        if len(parts) < 3:
            continue

        # 空行をチェック
        if not line:
            print("未計測期間があります。")
            return formattedLines

        date = line.split(',')[0]
        year = date[0:4]
        month = date[5:7]
        id = year + month
        dataValue = parts[2].strip()
        
        if not dataValue:
            dataValue = "-9999.9"

        # 辞書にIDが存在するかチェック
        if id not in idData:
            idData[id] = {
                'year': year,
                'month': month,
                'rainfall': [],
                'errorCount': 0
            }
        
        # 既存のリストにデータを追加
        idData[id]['rainfall'].append(dataValue)

        is_error = (dataValue == "-9999.9")
        if is_error:
            idData[id]['errorCount'] += 1

    return idData


def reviseData(idData,filename):
    sortedDict = {}
    revisedData = {}

    for id, dataDict in idData.items():
        dataList = dataDict['rainfall']
        
        sortedList = sorted(dataList, key = float, reverse = True)
        
        sortedDict[id] = {
            'year': dataDict['year'],
            'month': dataDict['month'],
            'rainfall': sortedList,
            'errorCount': dataDict['errorCount']
        }

    # ソートされたデータを用いて、以下の処理を実行
    for currentId, currentData in sortedDict.items():
        currentMonth = currentData['month']
        currentErrorCount = currentData['errorCount']
        
        # 基準となるID以外の同じ月を持つデータを収集
        otherRainfall = {}
        if currentErrorCount != 0:
            reviseFlag = False
            for otherId, otherData in sortedDict.items():
                if otherId != currentId and otherData['month'] == currentMonth:
                    otherRainfall[otherId] = [float(x) for x in otherData['rainfall']]
                    if otherData['month'] == '02':
                        otherYear = int(otherData['year'])
                        is_leap = (otherYear % 4 == 0 and otherYear % 100 != 0) or (otherYear % 400 == 0)
                        if not is_leap:
                            for _ in range(24):
                                otherRainfall[otherId].append("-9999.9")
                    if otherData['errorCount'] == 0 and reviseFlag == False:
                        reviseFlag = True
            
            print(f"'{filename}'{currentId}を修正します。")

            otherIdAverages = calcAverage(otherRainfall, reviseFlag, currentId)

            currentRainfall = currentData['rainfall']
            sortedDifferences = calcDifference(otherIdAverages, currentRainfall)

            # ここから降雨量の修正
            positiveAveragesCount = len([x for x in otherIdAverages if x > 0])
            positiveRainfallCount = len([x for x in currentRainfall if x > 0])
            # 降雨時間の最大値を平均の降雨時間とする
            jMax = positiveAveragesCount - positiveRainfallCount
            
            revisedCurrentRainfall = []
            j = 0
            k = 0
            for i in range(len(currentRainfall)):
                if currentRainfall[i] == -9999.9:
                    if j < jMax:
                        if sortedDifferences[k][1]:
                            revisedRainfall = sortedDifferences[k][1]
                        else:
                            revisedRainfall = 0.0
                        k += 1
                    else:
                        revisedRainfall = 0.0
                    j += 1

                else:
                    revisedRainfall = currentRainfall[i]
                revisedCurrentRainfall.append(revisedRainfall)
    
            revisedCurrentRainfall.sort(key = float, reverse = True)
            revisedData[currentId] = revisedCurrentRainfall

        else:
            dataList = idData[currentId]['rainfall']
            revisedData[currentId] = dataList

    return revisedData


def revise(filename,lines):
    # ファイルのデータを年月(YYYYMM)ごとに仕分け
    idData = formatLines(lines)
    # 欠損データの補完
    revisedData = reviseData(idData,filename)

    monthlySortedData = sortData(revisedData)

    return monthlySortedData

if __name__ =='__main__':
    revise()