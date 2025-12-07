import get_filename
import SSDB_error_revise
import d4PDF_sort
import count_rainfall
import d4PDF_bias_correction
import export_result

SSDB_ORG_DIR = './SSDB_org/'
D4PDF_ORG_DIR = './d4PDF_org/'
EXPORT_DIR = './results/'
# exportFileName = "{元のファイル名}_bc.txt"



def main():
    # 水門水質データベース降雨データの読み込み
    file_list_SSDB = get_filename.get(SSDB_ORG_DIR)
    for file_SSDB in file_list_SSDB:
        if file_SSDB.endswith('.txt'):
            with open(SSDB_ORG_DIR+file_SSDB,'r',encoding='UTF-8') as f:
                lines = f.readlines()
            f.close
            # 欠損データの補完と、月ごとで配列を作成しデータをソート
            revised_dict_SSDB = SSDB_error_revise.revise(file_SSDB,lines)
            export_result.export(EXPORT_DIR,file_SSDB,revised_dict_SSDB)
        else:
            print(f"{file_SSDB}は'.txt'ファイルではありません。")

    # 水門水質データベースの降水量ごとの出現回数をカウント
    rainfall_val_SSDB = count_rainfall.make_dict(revised_dict_SSDB)

    # d4PDF降雨データの読み込み
    file_list_d4PDF = get_filename.get(D4PDF_ORG_DIR)
    for file_d4PDF in file_list_d4PDF:
        if file_d4PDF.endswith('.txt'):
            with open(D4PDF_ORG_DIR+file_d4PDF,'r',encoding='UTF-8') as f:
                lines = f.readlines()
            f.close
            # 月ごとで配列を作成。
            sorted_dict_d4PDF = d4PDF_sort.sort(file_d4PDF,lines)
        else:
            print(f"{file_d4PDF}は'.txt'ファイルではありません。")
    
        # d4PDFのバイアス補正
        bc_dict_d4PDF = d4PDF_bias_correction.correction(sorted_dict_d4PDF, rainfall_val_SSDB)

        # 補正後データのエクスポート
        export_result.export(EXPORT_DIR,file_d4PDF,bc_dict_d4PDF)


if __name__ == '__main__':
    main()