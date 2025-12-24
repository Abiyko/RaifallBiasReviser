from datetime import datetime, timedelta

def sort(filename,lines):
    START_DATE_STR = '1991010101'
    START_DATETIME = datetime.strptime(START_DATE_STR, "%Y%m%d%H")

    processed_lines = []
    
    # 各データ行を処理
    for line in lines[1:]:
        parts = line.strip().split(',') 

        try:
            # 2. 連番を取得し、数値型に変換
            index = int(parts[0].strip()) # 前後の空白を削除してから数値変換
            
            # 3. 時刻データの計算
            elapsed_hours = index - 1
            current_datetime = START_DATETIME + timedelta(hours=elapsed_hours)
            if current_datetime.hour == 0:
                hour_str = '24'
                date_for_24h = current_datetime - timedelta(days=1)
                date_str = date_for_24h.strftime("%Y%m%d")
                timestamp_str = date_str + hour_str
            else:
                timestamp_str = current_datetime.strftime("%Y%m%d%H")
            
            new_line = f"{line.strip()},{timestamp_str}"
            
            processed_lines.append(new_line)

        except Exception as e:
            print(f"予期せぬエラー ({filename}, 行: {line.strip()}): {e}")

    processed_filedict = {}
    processed_filedict[filename] = '\n'.join(processed_lines)

    for filename, content_str in processed_filedict.items():
        file_monthly_data = {}
        lines = content_str.strip().split('\n')

        for line in lines:
            if not line:
                continue
            parts = line.strip().split(',')
            
            if len(parts) >= 3:
                timestamp_str = parts[2].strip()
                
                try:
                    if len(timestamp_str) >= 6:
                        month = timestamp_str[4:6]
                    else:
                        raise ValueError("時刻データの形式が不正です。")
                    
                    if month not in file_monthly_data:
                        file_monthly_data[month] = []
                    
                    rainfall_value = float(parts[1].strip())
                    file_monthly_data[month].append(rainfall_value)
                    
                except ValueError as e:
                    print(f"警告: ファイル {filename} の行 '{line.strip()}' の時刻データ解析に失敗しました ({e})。スキップします。")
                    continue
                
        for month in file_monthly_data:
            file_monthly_data[month].sort(key = float, reverse = True)

        return file_monthly_data


if __name__ == '__main__':
    sort()