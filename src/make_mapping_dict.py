import numpy as np
from multiprocessing import Pool, cpu_count

def interpolate_month_data(month_data_tuple, STEP):
    month, month_dict = month_data_tuple
    sorted_keys = sorted(month_dict.keys())
    
    # 補間ロジック
    for i, key_value in enumerate(sorted_keys):
        if month_dict[key_value] is None:
            # V_prev の検索
            i_prev = -1
            for j in range(i - 1, -1, -1):
                if month_dict[sorted_keys[j]] is not None:
                    i_prev = j
                    break
            
            # V_next の検索
            i_next = -1
            for j in range(i + 1, len(sorted_keys)):
                if month_dict[sorted_keys[j]] is not None:
                    i_next = j
                    break

            if i_prev != -1 and i_next != -1:
                # 補間が可能
                min_val = month_dict[sorted_keys[i_prev]]
                max_val = month_dict[sorted_keys[i_next]]

                m = i - i_prev
                n = i_next - i
                
                # 線形補間の計算
                raw_correcting_value = m / (m + n) * max_val + n / (m + n) * min_val
                
                # STEP 精度で丸める
                correcting_value = np.round(raw_correcting_value, STEP)
                
                month_dict[key_value] = correcting_value
            # 外挿領域は None のまま
            
    return (month, month_dict) # 処理結果をタプルで返す


def make(STEP, dict_before_correction, dict_after_correction):
    mapping_dict = {}
    final_mapping_dict = {}

    step = 10**-STEP
    
    for month in dict_before_correction.keys():
        mapping_dict[month] = dict(zip(dict_before_correction[month], dict_after_correction[month]))
        
        # 最大値の特定
        if not dict_before_correction[month]: continue
        max_recorded_value = np.round(max(dict_before_correction[month]), STEP)
        
        # stepsの生成
        stop_value = max_recorded_value + step / 2 
        steps = np.round(np.arange(0.0, stop_value, step), STEP)
        
        # 初期化
        initial_mapping = {float(x): None for x in steps}
        final_mapping_dict[month] = initial_mapping

        # 既知の値の代入と丸め
        for before_val, after_val in mapping_dict[month].items():
            rounded_before_val = np.round(before_val, STEP)
            rounded_after_val = np.round(after_val, STEP)
            
            if rounded_before_val in final_mapping_dict[month]:
                final_mapping_dict[month][rounded_before_val] = rounded_after_val

    # 処理すべきデータのリストを作成 [(month_key, month_dict), ...]
    data_to_process = [(month, month_dict) for month, month_dict in final_mapping_dict.items()]
    
    # 利用可能なCPUコア数を取得
    num_cores = cpu_count()
    # print(f"並列処理に {num_cores} コアを使用します。")
    
    # Poolを作成し、並列処理を開始（安全のため利用するCPUコア数にマイナス1の制限を設ける）
    with Pool(processes=num_cores - 1) as pool:
        # interpolate_month_data に data_to_process の各要素と STEP をマップ
        results = pool.starmap(interpolate_month_data, [(data, STEP) for data in data_to_process])

    # 処理結果を結合し、最終辞書を更新
    final_mapping_dict_parallel = {}
    for month, month_dict in results:
        final_mapping_dict_parallel[month] = month_dict
    
    return final_mapping_dict_parallel


if __name__ == '__main__':
    make()