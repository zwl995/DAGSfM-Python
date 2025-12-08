"""
Unit tests for the partition module
"""

import sys
import os
import tempfile
import sqlite3
import numpy as np

# Add the project root directory to the path so we can import dagsfm modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from dagsfm.partition import NcutPartitioner


def test_ncut_partitioner():
    """
    Test NcutPartitioner with configured database path
    """
    print("Testing N-cut Partitioner")
    print("=" * 30)
    
    # 检查是否已配置路径
    if DATABASE_PATH == "/path/to/your/database.db":
        print("请先在文件顶部配置实际的数据库路径！")
        return False
    
    # 检查数据库文件是否存在
    if not os.path.exists(DATABASE_PATH):
        print(f"错误：找不到数据库文件 '{DATABASE_PATH}'")
        return False
    
    print(f"数据库路径: {DATABASE_PATH}")
    
    # try:
    # 创建分区器
    partitioner = NcutPartitioner(DATABASE_PATH, "config/config.yaml")
    
    # 加载数据库
    print("正在加载数据库...")
    partitioner.load_database()
    print(f"成功加载 {len(partitioner.images)} 张图像")
    
    # 计算相似度矩阵
    print("正在计算相似度矩阵...")
    similarity_matrix, nodes = partitioner.compute_similarity_matrix()
    print(f"相似度矩阵大小: {similarity_matrix.shape}")
    
    # 执行标准化切割
    print("正在进行标准化切割...")
    clusters = partitioner.normalized_cut(k=10)
    print(f"生成 {len(clusters)} 个簇")
    for cluster_id, cluster in clusters.items():
        print(f"Cluster {cluster_id}: {len(cluster)} images")
    # print(f"clusters: {clusters}")
    
    # 扩展分区
    print("正在扩展分区...")
    expanded_clusters = partitioner.expand_partitions(clusters)
    print(f"扩展后的分区数量: {len(expanded_clusters)}")
    for cluster_id, cluster in expanded_clusters.items():
        print(f"Cluster {cluster_id}: {len(cluster)} images")
    print("分区扩展完成")

    # 保存子块图像列表
    submodel_files = partitioner.save_submodel_image_lists("./my_submodels")
    
    # # 完整场景分区
    # print("正在进行完整场景分区...")
    # partitions = partitioner.partition_scene(k=2, expansion_ratio=0.3)
    # print(f"最终分区数量: {len(partitions)}")
    
    # print("N-cut 分区测试完成！")
    # return True
        
    # except NotImplementedError:
    #     print("N-cut 分区功能尚未实现")
    #     return False
    # except Exception as e:
    #     print(f"N-cut 分区过程中发生错误: {e}")
    #     return False


if __name__ == '__main__':
    # 配置测试路径 - 运行时会自动创建测试数据库
    DATABASE_PATH = f"/ws/18_nfs/zwl/Data/DJI/jimeimigu/database_dagsfm_python.db"  # 会在运行时创建临时数据库
    success = test_ncut_partitioner()
    if not success:
        sys.exit(1)