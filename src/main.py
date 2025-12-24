import get_filename
import SSDB_error_revise
import d4PDF_sort
import count_rainfall
import d4PDF_bias_correction
import export_result
import export_map
import make_mapping_dict
import make_ave_map

SSDB_ORG_DIR = './data/SSDB_org/'
D4PDF_ORG_DIR = './data/d4PDF_org/'
EXPORT_DIR = './outputs/'
# exportFileName = "{元のファイル名}_bc.csv"
STEP = 2


def main():
    # ファイルリストの取得
    file_list_SSDB = get_filename.get(SSDB_ORG_DIR)
    file_list_d4PDF = get_filename.get(D4PDF_ORG_DIR)

    # 観測地点バイアス補正辞書の初期化
    avg_map_dicts = {}

    # 水門水質データベース降雨データの読み込み
    for file_SSDB in file_list_SSDB:
        # 地点が変わるたびに辞書を初期化
        bc_mapping_dict = {}

        if file_SSDB.endswith('.txt'):
            point_name = file_SSDB.split("_")[0]
            with open(SSDB_ORG_DIR+file_SSDB,'r',encoding='UTF-8') as f:
                lines = f.readlines()
            # 欠損データの補完と、月ごとで配列を作成しデータをソート
            revised_dict_SSDB = SSDB_error_revise.revise(file_SSDB,lines)
            # 補正後データのエクスポート
            # export_result.export(EXPORT_DIR,file_SSDB,revised_dict_SSDB)

            # 水門水質データベースの降水量ごとの出現回数をカウント
            rainfall_val_SSDB = count_rainfall.make_dict(revised_dict_SSDB)

            # d4PDF降雨データの読み込み
            correction_list_d4PDF = []
            for file_name_d4PDF in file_list_d4PDF:
                if file_name_d4PDF.split("_")[0] == point_name:
                    correction_list_d4PDF.append(file_name_d4PDF)

            for file_d4PDF in correction_list_d4PDF:
                if file_d4PDF.endswith('.txt'):
                    with open(D4PDF_ORG_DIR+file_d4PDF,'r',encoding='UTF-8') as f:
                        lines = f.readlines()
                    # 月ごとで配列を作成。
                    sorted_dict_d4PDF = d4PDF_sort.sort(file_d4PDF,lines)

                    # 補正後データのエクスポート
                    # export_result.export(EXPORT_DIR,file_d4PDF,sorted_dict_d4PDF)
                else:
                    print(f"{file_d4PDF}は'.txt'ファイルではありません。")
            
                # d4PDFのバイアス補正
                bc_dict_d4PDF = d4PDF_bias_correction.correction(sorted_dict_d4PDF, rainfall_val_SSDB)
                # 補正後データのエクスポート
                # export_result.export(EXPORT_DIR,file_d4PDF,bc_dict_d4PDF)
                
                bc_mapping_dict[file_d4PDF] = make_mapping_dict.make(STEP,sorted_dict_d4PDF,bc_dict_d4PDF)
                # シナリオごとバイアス補正マップデータのエクスポート
                # export_map.export(EXPORT_DIR,file_d4PDF,bc_mapping_dict[file_d4PDF])

            avg_map_dict = make_ave_map.make(STEP,bc_mapping_dict)
            # 観測地点ごとバイアス補正マップデータのエクスポート
            export_map.export(EXPORT_DIR,point_name,avg_map_dict)
            # export_map.export_pickle(EXPORT_DIR,point_name,avg_map_dict)
            # avg_map_dicts[point_name] = avg_map_dict
        else:
            print(f"{file_SSDB}は'.txt'ファイルではありません。")

        # print(avg_map_dicts.keys())


if __name__ == '__main__':
    main()