import numpy as np
from collections import defaultdict

def make(STEP, bc_mapping_dict):
    monthly_maps = defaultdict(dict)
    all_scenario_keys = list(bc_mapping_dict.keys())

    # 構造の変換
    for scenario_key, months in bc_mapping_dict.items():
        for month_key, data_dict in months.items():
            monthly_maps[month_key][scenario_key] = list(data_dict.values())
    
    monthly_avg_dict = {}

    # 刻み幅の計算
    delta = 10 ** -STEP

    # 月ごとに処理
    for month_key, scenarios_in_month in monthly_maps.items():
        
        # シナリオの欠損補完
        for s_key in all_scenario_keys:
            if s_key not in scenarios_in_month:
                scenarios_in_month[s_key] = []

        # パディング処理
        lengths = [len(v) for v in scenarios_in_month.values()]
        max_length = max(lengths) if lengths else 0
        for s_key in scenarios_in_month:
            current_list = scenarios_in_month[s_key]
            current_list.extend([-1] * (max_length - len(current_list)))

        # 平均値の算出
        averaged_list = []
        for values_at_index in zip(*scenarios_in_month.values()):
            org_value_sum = 0
            count = 0
            for value in values_at_index:
                if value != -1:
                    org_value_sum += value
                    count += 1
            average = org_value_sum / count if count > 0 else -1
            correcting_value = np.round(average, STEP)
            averaged_list.append(correcting_value)
            
        # 累積最大値の算出
        cumulative_max_list = []
        current_max = -1
        for value in averaged_list:
            current_max = max(current_max, value)
            cumulative_max_list.append(current_max)

        # 指定されたSTEP刻みの辞書形式へ変換
        monthly_avg_dict[month_key] = {
            round(i * delta, STEP): val for i, val in enumerate(cumulative_max_list)
        }

    return monthly_avg_dict


if __name__ == '__main__':
    make()