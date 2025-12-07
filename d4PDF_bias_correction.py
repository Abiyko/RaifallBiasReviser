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
            edit_array_d4PDF = np.array(monthly_list_d4PDF[int(current_start_index): int(end_index)])

            current_start_index = end_index

            # 補正範囲の最小値を求める
            min_val_edit_d4PDF = edit_array_d4PDF[-1]

            # 補正範囲の最大値を求める
            max_val_edit_d4PDF = edit_array_d4PDF[0]

            # 補正範囲の中央値を求める
            if len(edit_array_d4PDF) % 2 == 0:
                upper_median_index = len(edit_array_d4PDF) // 2
                lower_median_index = upper_median_index - 1
                upper_median_value = edit_array_d4PDF[upper_median_index]
                lower_median_value = edit_array_d4PDF[lower_median_index]
                median_val_d4PDF = (lower_median_value + upper_median_value) / 2
            else:
                median_index = len(edit_array_d4PDF) // 2
                median_val_d4PDF = edit_array_d4PDF[median_index]
            
            if len(edit_array_d4PDF) == 1 or max_val_edit_d4PDF - min_val_edit_d4PDF == 0:
                if median_val_d4PDF == 0:
                    magnification = 0
                else:
                    magnification = value_SSDB / median_val_d4PDF

                corrected_array = edit_array_d4PDF * magnification
                
            else:
                slope = 1 / (max_val_edit_d4PDF - min_val_edit_d4PDF)
                intercept = value_SSDB - median_val_d4PDF / (max_val_edit_d4PDF - min_val_edit_d4PDF)
                corrected_array = edit_array_d4PDF * slope + intercept

                #クリッピング
                clip_min = value_SSDB - 0.5
                clip_max = value_SSDB + 0.5
                corrected_array = np.clip(corrected_array, clip_min, clip_max)

            bc_dict_d4PDF[month].extend(corrected_array)

    return bc_dict_d4PDF

if __name__ == '__main__':
    correction()