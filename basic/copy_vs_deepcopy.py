
import random
import copy


def get_hit_by_gap(pools, shoots, hits, gap):
    index = 0
    in_range = False
    for index_p, curr_p in enumerate(pools):
        target = shoots[index]

        # 收集區間
        if (target - gap) <= curr_p <= (target + gap):
            in_range = True
            hits[target]["index"].append(index_p)
            hits[target]["candi"].append(curr_p)
        else:
            # 區間外了往下一段
            if in_range and curr_p > (target + gap):
                index += 1
                if index >= len(hits):
                    break
            in_range = False
    return hits


if __name__ == "__main__":
    gap = 2
    pools = [i + round(random.uniform(0, 1), 1) for i in range(100)]
    shoots = [random.randint(0, 100) for _ in range(5)]
    shoots.sort()

    hit = {"index": [], "candi": []}
    # 注意需要使用 deepcopy，避免使用相同記憶體位置
    hits = {shoot: copy.deepcopy(hit) for shoot in shoots}

    hits = get_hit_by_gap(pools, shoots, hits, gap)
    
    print("pools\n", pools)
    print("shoots\n", shoots)
    print("hits1\n", hits)

    # ---- 錯誤示範 ----
    # 當深層的結構，使用 copy，只有表層位置複製，內部結構依舊是同一份記憶體位置
    hits = {shoot: hit.copy() for shoot in shoots}

    hits = get_hit_by_gap(pools, shoots, hits, gap)
    
    # print(pools)
    # print(shoots)
    print("hits2\n", hits)
