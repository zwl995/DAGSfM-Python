"""
使用N-cut算法进行场景分割的模块
"""
import yaml
import pycolmap
import numpy as np
import networkx as nx
from sklearn.cluster import SpectralClustering


class NcutPartitioner:
    """
    使用归一化割(N-cut)算法对场景进行分割。
    使用数据库路径初始化以加载图像匹配数据。
    """
    
    def __init__(self, database_path, config_path=None):
        """
        使用数据库路径初始化N-cut分割器
        
        Args:
            database_path (str): COLMAP数据库文件的路径
        """
        self.database_path = database_path
        self.graph = nx.Graph()
        self.images = {}  # image_id -> image_name
        self.lost_egdes = []
        self.clusters = {}
        self.expanded_clusters = {}

        # 默认配置参数
        self.config = {
            'ncut_k': 5,
            'expansion_ratio': 0.2,
            'max_image_overlap': 5,
            'completeness_ratio': 0.8
        }
        
        # 如果提供了配置文件路径，则加载配置
        if config_path:
            self.load_config(config_path)
    
    def load_config(self, config_path):
        """
        从YAML文件加载配置
        
        Args:
            config_path (str): YAML配置文件的路径
        """
        try:
            with open(config_path, 'r') as f:
                loaded_config = yaml.safe_load(f)
                if loaded_config:
                    self.config.update(loaded_config)
            print(f"配置已从 {config_path} 加载")
        except FileNotFoundError:
            print(f"未找到配置文件 {config_path}。使用默认参数。")
        except Exception as e:
            print(f"加载配置文件时出错: {e}。使用默认参数。")

    def load_database(self):
        """
        从COLMAP数据库加载数据并构建初始视图图
        """
        # 使用pycolmap加载数据库
        db = pycolmap.Database(self.database_path)
        
        # 读取所有图像
        images = db.read_all_images()

        # 将图像ID和名称添加到self.images字典中，并添加为图的节点
        for image in images:
            self.images[image.image_id] = image.name
            self.graph.add_node(image.image_id, name=image.name)
        
        # 为图添加有权边，匹配内点数量作为权重
        pair_ids, two_view_geometries = db.read_two_view_geometries()
        for i, pair_id in enumerate(pair_ids):
            pair = db.pair_id_to_image_pair(pair_id)
            inlier_count = len(two_view_geometries[i].inlier_matches)
            self.graph.add_edge(pair[0], pair[1], weight=inlier_count)
            
        # 打印图的相关信息
        print(f"图信息:")
        print(f"  节点数(图像): {self.graph.number_of_nodes()}")
        print(f"  边数(匹配): {self.graph.number_of_edges()}")
        if self.graph.number_of_nodes() > 0:
            degrees = [degree for _, degree in self.graph.degree()]
            print(f"  平均节点度数: {np.mean(degrees):.2f}")
            print(f"  最大节点度数: {np.max(degrees)}")
            print(f"  最小节点度数: {np.min(degrees)}")
    
    def compute_similarity_matrix(self):
        """
        根据视图图中的内点数计算相似性矩阵
        
        Returns:
            np.ndarray: 大小为(n, n)的相似性矩阵，其中n是节点数
            list: 与矩阵索引对应的节点ID列表
        """
        nodes = list(self.graph.nodes())
        n = len(nodes)
        node_to_idx = {node: idx for idx, node in enumerate(nodes)}
        
        # 初始化相似性矩阵
        similarity_matrix = np.zeros((n, n))
        
        # 填充相似性值
        for node1, node2, data in self.graph.edges(data=True):
            i, j = node_to_idx[node1], node_to_idx[node2]
            weight = data.get('weight', 0)
            similarity_matrix[i, j] = weight
            similarity_matrix[j, i] = weight  # 对称矩阵
            
        return similarity_matrix, nodes
    
    def normalized_cut(self, k):
        """
        使用谱聚类执行归一化割聚类
        
        Args:
            k (int): 聚类/分区数
            
        Returns:
            dict: cluster_id到该聚类中image_ids列表的映射
        """
        # 如果尚未加载数据，则加载数据
        if self.graph.number_of_nodes() == 0:
            self.load_database()
            
        # 获取相似性矩阵
        similarity_matrix, nodes = self.compute_similarity_matrix()
        
        # 处理k大于节点数的情况
        num_nodes = len(nodes)
        if k > num_nodes:
            k = num_nodes
            
        # 执行谱聚类
        spectral = SpectralClustering(
            n_clusters=k,
            affinity='precomputed',
            assign_labels='discretize',
            random_state=42
        )
        
        # 拟合聚类模型
        cluster_labels = spectral.fit_predict(similarity_matrix)
        
        # 按聚类分组节点
        for i, label in enumerate(cluster_labels):
            if label not in self.clusters:
                self.clusters[label] = []
            self.clusters[label].append(nodes[i])
        
        # 创建节点ID到数组索引的映射
        node_to_idx = {node: idx for idx, node in enumerate(nodes)}

        # 创建节点到聚类ID的映射
        node_to_cluster = {}
        for cluster_id, node_list in self.clusters.items():
            for node in node_list:
                node_to_cluster[node] = cluster_id

        # 3. 找出所有割边 (丢失的边)
        for u, v, data in self.graph.edges(data=True):
            # 通过映射获取正确的数组索引
            idx_u, idx_v = node_to_idx[u], node_to_idx[v]
            if cluster_labels[idx_u] != cluster_labels[idx_v]:
                # 存储边信息：(节点u, 节点v, 节点u的cluster_id, 节点v的cluster_id, 边权重)
                edge_info = (
                    u,  # 节点u的ID
                    v,  # 节点v的ID
                    node_to_cluster[u],  # 节点u所属的cluster ID
                    node_to_cluster[v],  # 节点v所属的cluster ID
                    data.get('weight', 1.0)  # 边的权重
                )
                self.lost_egdes.append(edge_info)

        return self.clusters
    
    def expand_partitions(self, clusters):
        """
        通过包含相邻节点来扩展分区，基于边权重
        
        Args:
            clusters (dict): cluster_id到image_ids列表的映射
            expansion_ratio (float): 添加到每个聚类的邻居比例
            
        Returns:
            dict: 扩展后的聚类，包含额外的相邻节点
        """
        # 初始化expanded_clusters为原始clusters的副本
        self.expanded_clusters = {}
        for cluster_id, nodes in clusters.items():
            self.expanded_clusters[cluster_id] = list(nodes)  # 使用list保持一致性
        
        # 首先建立cluster之间的连接关系并收集丢失的边
        cluster_connections = {}  # 存储cluster对之间的连接信息 {(cluster1_id, cluster2_id): [lost_edges]}
                
        # 遍历所有丢失的边，建立cluster间的连接关系
        for u, v, cu, cv, weight in self.lost_egdes:
            # 确保cluster对的顺序一致，避免重复 (cluster1_id, cluster2_id) 和 (cluster2_id, cluster1_id)
            cluster_pair = tuple(sorted([cu, cv]))
            
            # 初始化cluster对的丢失边列表
            if cluster_pair not in cluster_connections:
                cluster_connections[cluster_pair] = []
            
            # 添加丢失的边信息 (节点u, 节点v, 边权重)
            cluster_connections[cluster_pair].append((u, v, weight))

        # 遍历所有有连接的cluster对，添加丢失的边
        for cluster_pair, lost_edges in cluster_connections.items():
            cluster1_id, cluster2_id = cluster_pair
            # 调用方法在cluster之间添加丢失的边
            self.add_lost_edges_between_clusters(
                cluster1_id, 
                cluster2_id, 
                lost_edges
            )
        
        return self.expanded_clusters
    
    def partition_scene(self, k=None, expansion_ratio=None):
        """
        将场景分割成可管理的块以进行SfM处理
        
        Args:
            k (int): N-cut分区的聚类数
            expansion_ratio (float): 用于通过邻居扩展聚类的比例
            
        Returns:
            dict: 最终分区，包含扩展后的聚类
        """
        # 使用配置中的默认值或传入的参数
        if k is None:
            k = self.config['ncut_k']
        if expansion_ratio is None:
            expansion_ratio = self.config['expansion_ratio']

        # 如果尚未加载数据，则加载数据
        if self.graph.number_of_nodes() == 0:
            self.load_database()
        
        # 执行N-cut分区
        clusters = self.normalized_cut(k)
        
        # 扩展分区
        expanded_clusters = self.expand_partitions(clusters, self.config["expansion_ratio"])
        
        return expanded_clusters
    
    def add_lost_edges_between_clusters(self, cluster1_id, cluster2_id, lost_edges_between_clusters, max_image_overlap=5, completeness_ratio=0.8):
        """
        在两个聚类之间添加丢失的边，以提高完整性比率并满足图像重叠约束。
        
        Args:
            cluster1_id (int): 第一个聚类的ID
            cluster2_id (int): 第二个聚类的ID
            lost_edges_between_clusters (list): 连接两个聚类的丢失边列表，每个元素为(u, v, weight)元组
            max_image_overlap (int): 最大图像重叠数
            completeness_ratio (float): 完整性比率阈值
            
        Returns:
            tuple: 更新后的两个聚类 (cluster1_images, cluster2_images)
        """
        # 使用配置中的默认值或传入的参数
        if max_image_overlap is None:
            max_image_overlap = self.config['max_image_overlap']
        if completeness_ratio is None:
            completeness_ratio = self.config['completeness_ratio']

        # 获取两个聚类的图像集合
        cluster1_images = set(self.expanded_clusters[cluster1_id])
        cluster2_images = set(self.expanded_clusters[cluster2_id])
        
        # 计算共同图像数量，如果超过最大重叠则返回
        common_images = cluster1_images.intersection(cluster2_images)
        if len(common_images) > max_image_overlap:
            return list(cluster1_images), list(cluster2_images)
        
        # 检查是否已经满足完整性比率
        if self._is_satisfy_completeness_ratio(cluster1_images, cluster1_id, completeness_ratio) and \
        self._is_satisfy_completeness_ratio(cluster2_images, cluster2_id, completeness_ratio):
            return list(cluster1_images), list(cluster2_images)
        
        # 按权重降序排序
        lost_edges_between_clusters.sort(key=lambda edge: edge[2], reverse=True)
        
        # 添加丢失的边
        for u, v, weight in lost_edges_between_clusters[:max_image_overlap]:
            # 确定哪个节点属于哪个聚类
            if u in cluster1_images or v in cluster1_images:
                added_image_for_cluster1 = u if u not in cluster1_images else v
                added_image_for_cluster2 = u if u not in cluster2_images else v
            else:
                added_image_for_cluster1 = u if u not in cluster2_images else v
                added_image_for_cluster2 = u if u not in cluster1_images else v
                
            # 选择较小的聚类来添加图像，避免大的聚类变得过大
            selected_cluster = cluster2_images if len(cluster1_images) > len(cluster2_images) else cluster1_images
            selected_cluster_id = cluster2_id if len(cluster1_images) > len(cluster2_images) else cluster1_id
            
            # 添加图像到未满足完整性比率的聚类中
            if selected_cluster is cluster1_images:
                if not self._is_satisfy_completeness_ratio(cluster1_images, cluster1_id, completeness_ratio) and added_image_for_cluster1 not in cluster1_images:
                    cluster1_images.add(added_image_for_cluster1)
            else:
                if not self._is_satisfy_completeness_ratio(cluster2_images, cluster2_id, completeness_ratio) and added_image_for_cluster2 not in cluster2_images:
                    cluster2_images.add(added_image_for_cluster2)
                    
            # 如果两个聚类都满足完整性比率，则提前返回
            if self._is_satisfy_completeness_ratio(cluster1_images, cluster1_id, completeness_ratio) and \
            self._is_satisfy_completeness_ratio(cluster2_images, cluster2_id, completeness_ratio):
                break
        
        # 更新expanded_clusters
        self.expanded_clusters[cluster1_id] = list(cluster1_images)
        self.expanded_clusters[cluster2_id] = list(cluster2_images)
        
        return list(cluster1_images), list(cluster2_images)

    def _is_satisfy_completeness_ratio(self, cluster_images, cluster_id, completeness_ratio=0.8):
        """
        检查聚类是否满足完整性比率
        
        Args:
            cluster_images (set): 聚类中的图像集合
            cluster_id (int): 聚类ID
            completeness_ratio (float): 完整性比率阈值
            
        Returns:
            bool: 是否满足完整性比率
        """
        # 使用配置中的默认值或传入的参数
        if completeness_ratio is None:
            completeness_ratio = self.config['completeness_ratio']

        # 如果expanded_clusters为空或者当前聚类未初始化，则直接返回True
        if self.expanded_clusters is None or cluster_id not in self.expanded_clusters:
            return True
        
        # 计算重复节点数（与其他聚类的公共图像数量）
        repeated_node_num = 0
        for other_cluster_id, other_cluster_images in self.expanded_clusters.items():
            if cluster_id == other_cluster_id:
                continue
            # 计算当前聚类与其它聚类之间的公共图像数量
            common_images_num = len(set(cluster_images).intersection(set(other_cluster_images)))
            repeated_node_num += common_images_num
        
        # 计算重复比例
        cluster_size = len(cluster_images)
        if cluster_size == 0:
            return True
        
        repeated_ratio = repeated_node_num / cluster_size
        
        # 检查是否满足完整性比率
        return repeated_ratio > completeness_ratio

    def save_submodel_image_lists(self, output_dir="submodel_lists"):
        """
        将每个子模型的图像列表保存到单独的文本文件中。
        
        Args:
            output_dir (str): 保存子模型图像列表文件的目录
            
        Returns:
            dict: 子模型ID到其图像列表文件路径的映射
        """
        import os
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 用于存储子块文件路径的字典
        submodel_files = {}
        
        # 为每个扩展后的聚类（子块）创建图像列表文件
        for cluster_id, image_ids in self.expanded_clusters.items():
            # 创建子块文件名
            submodel_filename = os.path.join(output_dir, f"submodel_{cluster_id}_images.txt")
            submodel_files[cluster_id] = submodel_filename
            
            # 写入图像名称到文件
            with open(submodel_filename, 'w') as f:
                for image_id in image_ids:
                    if image_id in self.images:
                        f.write(self.images[image_id] + '\n')
            
            print(f"子模型 {cluster_id} 的图像列表已保存到: {submodel_filename} ({len(image_ids)} 张图像)")
        
        print(f"所有子模型图像列表已创建在 '{output_dir}' 目录中")
        return submodel_files