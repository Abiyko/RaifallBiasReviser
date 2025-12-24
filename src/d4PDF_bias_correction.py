import numpy as np

def correction(sorted_dict_d4PDF, rainfall_val_SSDB):
    bc_dict_d4PDF = {}
    for month in sorted_dict_d4PDF:
        bc_dict_d4PDF[month] = []
        monthly_list_d4PDF = sorted_dict_d4PDF[month]
        monthly_dict_SSDB = rainfall_val_SSDB[month]

        current_start_index = 0
        for value_SSDB,count_SSDB in monthly_dict_SSDB.items():
            if count_SSDB == 0:
                continue

            end_index = current_start_index + count_SSDB

            if value_SSDB == 0:
                # 配列i+1が存在しない場合(最後)では配列iの最小値はとして補正する配列を取得する
                do_pop = False
            else:
                # 配列i+1の最大値を配列iの最小値として補正する配列を取得する
                end_index += 1
                do_pop = True

            edit_array_d4PDF = np.array(monthly_list_d4PDF[int(current_start_index): int(end_index)])
            current_start_index = end_index

            # 補正範囲の最小値を求める
            min_val_edit_d4PDF = edit_array_d4PDF[-1]

            # 補正範囲の最大値を求める
            max_val_edit_d4PDF = edit_array_d4PDF[0]

            if max_val_edit_d4PDF - min_val_edit_d4PDF == 0:
                corrected_array = value_SSDB + edit_array_d4PDF * 0
            elif not do_pop :
                corrected_array = edit_array_d4PDF * 0
            elif value_SSDB == 1:
                corrected_min_val = value_SSDB - 1
                corrected_array = corrected_min_val + (edit_array_d4PDF - min_val_edit_d4PDF) / (max_val_edit_d4PDF - min_val_edit_d4PDF) * 1.5
            else:
                corrected_min_val = value_SSDB - 0.5
                corrected_array = corrected_min_val + (edit_array_d4PDF - min_val_edit_d4PDF) / (max_val_edit_d4PDF - min_val_edit_d4PDF)

            bc_dict_d4PDF[month].extend(corrected_array.astype(float).tolist())

            if do_pop:
                bc_dict_d4PDF[month].pop(-1)

    return bc_dict_d4PDF


if __name__ == '__main__':
    correction()