from pathlib import Path
import pickle
from pathlib import Path

def export(EXPORT_DIR, org_filename, corrected_data):
    filename = Path(org_filename).stem
    exportFileName = f"{EXPORT_DIR}{filename}_bc.csv"

    months = sorted(corrected_data.keys(), key=int) 

    if not months:
        print("エクスポートするデータがありません。")
        return

    max_rows = 0
    # 処理する月全てについて行数の最大値を取得
    for month_key in months:
        max_rows = max(max_rows, len(corrected_data[month_key]))
    
    month_data = {}
    for month_key in months:
        month_data[month_key] = list(corrected_data[month_key].items())
    
    with open(exportFileName, 'w', encoding='UTF-8') as f:

        # ヘッダー行の作成と出力
        header_row = []
        for month_key in months:
            month_num = int(month_key)
            month_name = f"{month_num:02d}"
            
            header_row.append(f"{month_name}_BEFORE")
            header_row.append(f"{month_name}_AFTER")
        
        f.write(",".join(header_row) + '\n')

        # データ行の出力
        for i in range(max_rows):
            row_data = []
            
            for month_key in months:
                current_month_list = month_data[month_key]
                
                before_val = ""
                after_val = ""

                # インデックス i が現在の月のデータリストの範囲内かを確認（IndexError対策）
                if i < len(current_month_list):
                    # month_data[month_key][i] はタプル (before_val, after_val)
                    before_val = current_month_list[i][0]
                    after_val = current_month_list[i][1]
                    
                    # None の場合は空欄に設定
                    if after_val is None:
                        after_val = ""
                    if before_val is None:
                        before_val = ""
                
                # 補正前の値（BEFORE）と補正後の値（AFTER）を続けて row_data に追加
                row_data.append(f"{before_val}")
                row_data.append(f"{after_val}")
            
            f.write(",".join(row_data) + '\n')
            
    print(f"{exportFileName} の出力に成功しました。")
    return


def export_pickle(EXPORT_DIR, org_filename, corrected_data):
    # ファイル名の準備
    filename = Path(org_filename).stem
    export_path = Path(EXPORT_DIR) / f"{filename}_bc.pkl"

    if not corrected_data:
        print(f"警告: {filename} のエクスポートするデータがありません。")
        return

    try:
        # バイナリ書き込みモード ('wb') で保存
        with open(export_path, 'wb') as f:
            pickle.dump(corrected_data, f)
        print(f"{export_path} (Pickle形式) の出力に成功しました。")
    except Exception as e:
        print(f"{filename} のエクスポート中に問題が発生しました: {e}")
            

if __name__ == '__main__':
    export()
    export_pickle()