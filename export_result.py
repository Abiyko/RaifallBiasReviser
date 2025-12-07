from pathlib import Path
import calendar



def export(EXPORT_DIR, org_filename,corrected_data):
    filename = Path(org_filename).stem
    exportFileName = f"{EXPORT_DIR}{filename}_bc.txt"

    f = open(exportFileName,'w',encoding='UTF-8')

    # データを列ごとにソートされた月のキー順に処理するため、キーを取得しソート
    months = sorted(corrected_data.keys())

    # ヘッダー行の作成と出力
    header_row = []
    for month_key in months:
        month_num = int(month_key)
        month_name = calendar.month_name[month_num]
        header_row.append(month_name)
    f.write(",".join(header_row) + '\n')

    max_rows = 0
    for month in months:
        max_rows = max(max_rows, len(corrected_data.get(month, [])))

    # データ行の出力
    for i in range(max_rows):
        row_data = []
        for month in months:
            data_list = corrected_data.get(month, [])
            if i < len(data_list):
                row_data.append(f"{data_list[i]}")
            else:
                row_data.append("") 
        
        f.write(",".join(row_data) + '\n')
    f.close
    print(f"{exportFileName}の出力に成功しました。")
            

if __name__ == '__main__':
    export()