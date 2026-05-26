#!/bin/bash
# WPS金山文档批量整理脚本 - 2026-04-16
# 前置：需设置 NODE_EXTRA_CA_CERTS=/etc/ssl/cert.pem

BASE="NODE_EXTRA_CA_CERTS=/etc/ssl/cert.pem mcporter call kdocs"

# ============================================================
# 文件夹ID映射（漫游箱drive_id=147562401，云文档drive_id=147559281）
# ============================================================

# 漫游箱文件夹
WYY_HJL=vFWQXnVyL1Mn8qNNvH5N1xrySsXEnjFSr   # 华检联公司治理
WYY_OCEAN=aNvjdgZXS1M868XSKd5K1xbL8FpqnxeKu # 海南海洋经济项目
WYY_PRICE=fv85K8A261MNCpi2dAzt1xXoAnE6SaPxC # 检测收费参考价
WYY_SURVEY=v8xpsrQ6KxMFBembtcBgxxeqzF9gzWGGs # 勘察与市场资料
WYY_BID=dUeAAU7errMK2wSP36RArxJMioexPBqDg   # 投标与报价
WYY_LEARN=vnA4xKnnmxMTfTG8gSMG1xhuWJWRCXVcg # 个人学习
WYY_WRITE=mRgzn5M72xM3wY4oHAZurxKLKAceMiqP  # 个人写作（实际ID：mRgzn5M72xM3wY4oHAZurxGKLKAceMiqP）
WYY_EXTERNAL=a23wvuCsjrMJn136nnZdrxEc7Z81J4Gde # 外部协作文件

# 云文档文件夹
YD_HJL=FmrmDVJaJrMoNYKoMUF5rxqQqZmrdYL83
YD_OCEAN=xUVQufZ1orMTFNB83ExkxxSvsjBajssmh
YD_PRICE=AQHJFktzw9MffDRfJwYi1xddj5baMFgNs
YD_SURVEY=rjgaFUvh11Min9jDMuTArxWsvPtmhUERn
YD_BID=MNkBXn8bJxM7HBTzCCNFrxwCKmEVyiE1h
YD_LEARN=bhHvwWuETxM16H6oPP75rxiKk8YCZ9tDu
YD_WRITE=jVA3gNpaJrMGpUEqw8yVxxVyhuUed4kz8
YD_EXTERNAL=RYnwwJuaJrMKxP4zXidHrxeMJ6zwYCcgZ

echo "=== 1. 移动漫游箱根目录文件 ==="

# 漫游箱：公司治理
$BASE move_file file_ids='["RJV6k24BY1MeGQpJqnkJrxMEWBhchpyGN","pYQdj43errMSeuXgtrcFrxS1RZ89a7Fgn","xT7MdXRZB1MYdLGjQAQqxxNLWrmstDUPo","4RZs4f6tbxMiUA7rQZYi1xKXZdKfmyeUr","dwsiHXw1q1MRywAsCrjjrxHmaE9jjwru7","h6HLX8xwE1MysW4SmVxkxx81BhsFKQ6Vn","8uC6SsuUP1MpLyTW5HamxxDgWLKg9U6pf","popwsctrK1MLrFL17b6ArxDZwqLJTCfuW","Pr69rDTUP1MQtf1nqfcgxx77AGTFwNqZr","ni8qZjwLvrMXiNADAHVK1xzhtEsVn6W2o","AU5rSqxLgrMaDfoa8S8PrxYfhVS8cyMvj","N2UnAEWVMrMJbezzRCnkrxGDnoXo1MNNN","d3FUZtgCurMbSfJ3N27i1x9oYBFum3VAu"]' dst_parent_id=$WYY_HJL
echo "漫游箱-公司治理完成"

# 漫游箱：海南海洋经济项目
$BASE move_file file_ids='["ng8g9r7TtxMu9Zmvr5dB1xkbArs3WXWku","d9iLEcSHfrMoquoZmjY4rxiW3UqmAKdkg","E168XRR891MsC1Uo8NW5rxqdwieBBQ7Ey","aRuYSMNJArMBJk6Z7Hndrx7iqdz83CXFB","ngqh5jRZB1MbVUs4x2iP1xNbDvrJwQdrY","4jVZnMDZD1M5ygCNfzQ1Bxg1bKMGKcVFr"]' dst_parent_id=$WYY_OCEAN
echo "漫游箱-海南海洋经济项目完成"

# 漫游箱：检测收费参考价
$BASE move_file file_ids='["tqJodG5TtxMfV9ZMEPv91x6CPkfE6BRpf"]' dst_parent_id=$WYY_PRICE
echo "漫游箱-检测收费参考价完成"

# 漫游箱：勘察与市场资料
$BASE move_file file_ids='["dLSevbHtbxMv56qYmQ9Zrx9RMFtcK5EjD","dBURUMf6qxMniqcZ1HbK1xFEjCPxzyHwD","ng8g9r7TtxMu9Zmvr5dB1xkbArs3WXWku"]' dst_parent_id=$WYY_SURVEY
echo "漫游箱-勘察与市场资料完成"

# 漫游箱：投标与报价
$BASE move_file file_ids='["d3FUZtgCurMbSfJ3N27i1x9oYBFum3VAu"]' dst_parent_id=$WYY_BID
echo "漫游箱-投标与报价完成"

# 漫游箱：个人学习
$BASE move_file file_ids='["m2XYET5x3rM42FLtv6RJrxXHM4EGdLRZr","n3F6Q1NSyrMQEGp6jdMkxxPMzWmGkNUF8","4bPM7ZkGRxM2zdEPVBJs1xa8DcV6NVr9B"]' dst_parent_id=$WYY_LEARN
echo "漫游箱-个人学习完成"

# 漫游箱：个人写作
$BASE move_file file_ids='["hcJFTA3XS1MH2epRsegB1xsvRHCn7kjvv","4RZs4f6tbxMiUA7rQZYi1xKXZdKfmyeUr"]' dst_parent_id=$WYY_WRITE
echo "漫游箱-个人写作完成"

# 漫游箱：外部协作文件
$BASE move_file file_ids='["txPUNwQh2xMzh7mkNfUfxx6CHyQJ6xeC7","brwrK9ELvrMAXni9BdzT1xa6dporx2nGC","8XeqLTtcHxMH2SDpDcQ8rxtVzZknL7XPb"]' dst_parent_id=$WYY_EXTERNAL
echo "漫游箱-外部协作文件完成"

echo "=== 2. 移动云文档根目录文件 ==="

# 云文档：检测收费参考价（清理子文件夹的收费参考价，保留漫游箱的版本）
# 先把子文件夹zL2MG12orxM9cgmRRF5T1xgABk9h6XbD3中的2025版收费参考价移到收费参考价文件夹
$BASE move_file file_ids='["Hz2AHTURpxMdJcU5G2aS1xWHVtgkgF9CD"]' dst_parent_id=$YD_PRICE
echo "云文档-收费参考价完成"

# 云文档：海南海洋经济项目（处理同名文件）
$BASE move_file file_ids='["AorogoCsjrM6HzPbZxSWxxCfHgd3D9TGs","xCFiwcdxFrMYvS8ByR9Zrxoy2XqLnodnb"]' dst_parent_id=$YD_OCEAN
echo "云文档-海南海洋经济项目完成"

# 云文档：勘察与市场资料
$BASE move_file file_ids='["hkBqgAoLgrMakc1o1NA91xnZ3goFzPi3C","aEYVV26ZB1MZJx4Dnbxb1xny59rUPEHBf","nXfrRaq1q1MaM33qDg6yrxQR414Y53dTv","h7UEHHJuk9Mm1yZ28kb3rxxwZgE3bD4Z1","xSP4k9ssjrM7ZrxS7xie1xpYy1sBLFB6j","nkEA28BQH9MbuGBkW9WFrxoiKXK6SxMJe","r8K1hWKBY1MLkhg4ecYN1xdy3aeSCMi5z"]' dst_parent_id=$YD_SURVEY
echo "云文档-勘察与市场资料完成"

# 云文档：华检联公司治理
$BASE move_file file_ids='["eCiJkEAVMrMGmjPdDyj11xggFLBB9rXuW","fasjrHSAxrM9kmrkiuMW1xbgE4ADUP5qJ","EGRpJEy4zxMdQWkszRz91xzjNv3MzkFn8"]' dst_parent_id=$YD_HJL
echo "云文档-公司治理完成"

# 云文档：投标与报价
$BASE move_file file_ids='["b2d7PCQ1q1MsMaJ2rieS1xb8xBrJ1JWn8"]' dst_parent_id=$YD_BID
echo "云文档-投标与报价完成"

# 云文档：外部协作文件
$BASE move_file file_ids='["b2d7PCQ1q1MsMaJ2rieS1xb8xBrJ1JWn8"]' dst_parent_id=$YD_EXTERNAL
echo "云文档-外部协作文件完成"

echo "=== 全部完成 ==="
