# DAGSfM-Python

DAGSfM-Python是一个基于Python的Structure from Motion (SfM)系统，采用有向无环图(DAG)方法优化三维重建过程。该项目利用图论中的N-cut算法对场景进行分割，然后并行处理各个子块，最后合并结果以获得完整的三维重建。

本项目是 [DAGSfM](https://github.com/AIBluefisher/DAGSfM) 的 Python 实现与优化版本，原项目由 Chen et al. 开发并用 C++ 实现。

## 项目架构

本项目采用模块化设计，主要包含以下几个核心模块：

```
DAGSfM-Python/
├── dagsfm/                 # 核心模块
│   ├── __init__.py         # 包初始化文件
│   ├── features.py         # 特征提取与匹配模块
│   ├── partition.py        # 场景分块模块（基于N-cut算法）
│   ├── reconstruction.py   # 子块重建模块
│   ├── merging.py          # 子块合并与BA模块
│   ├── pipeline.py         # CGraph工作流管理模块
│   └── utils.py            # 工具函数模块
├── tests/                  # 测试模块
│   ├── __init__.py         # 测试包初始化文件
│   ├── test_features.py    # 特征模块测试
│   ├── test_partition.py   # 分块模块测试
│   ├── test_reconstruction.py # 重建模块测试
│   ├── test_merging.py     # 合并模块测试
│   ├── test_pipeline.py    # 工作流模块测试
│   └── test_utils.py       # 工具模块测试
├── main.py                 # 主入口文件
├── run_tests.py            # 测试运行脚本
├── requirements.txt        # 项目依赖文件
└── README.md               # 项目说明文件
```

## 核心模块说明

### 1. 特征提取与匹配模块 [features.py]
负责从图像中提取特征点（如SIFT）并进行特征匹配，构建图像间的匹配关系图。

### 2. 场景分块模块 [partition.py]
基于N-cut算法对整个场景进行分割，将大型SfM问题分解为多个较小的子问题。该模块包含：
- ViewGraphNode类：表示图像节点
- ViewGraph类：管理视图图结构
- NcutPartitioner类：实现N-cut分割算法

### 3. 子块重建模块 [reconstruction.py]
使用pycolmap或colmap对分割后的子块进行独立重建。

### 4. 子块合并与BA模块 [merging.py]
将各个子块的重建结果进行配准和合并，并进行全局光束法平差(Bundle Adjustment)优化。

### 5. 工作流管理模块 [pipeline.py]
使用CGraph的Python版本管理系统整体工作流程和模块间依赖关系。

## TODO List

### 特征提取与匹配模块
- [✔] 集成SIFT特征提取(使用Colmap进行特征提取)
- [✔] 实现特征匹配功能(使用Colmap提供暴力匹配与空间匹配)
- [ ] 添加Hloc相关DL提点与匹配功能

### View-Graph维护模块
- [ ] 循环旋转误差过滤View-Graph
- [ ] 检测最大连通分量过滤View-Graph
- [ ] 使用全局旋转平均过滤View-Graph

### View-Graph分割与扩展模块
- [ ] 实现Ncut算法对View-Graph进行分割
- [ ] 基于分割后子块进行扩展

### 重建模块
- [ ] 实现子块单独重建(暂采用Colmap原天增量重建)

### 子模型合并模块
- [ ] 构建子模型图
- [ ] 检测图最大联通分量
- [ ] 使用Kruskal算法计算最小生成树
- [ ] 找到锚点，作为对齐参考

### 三角化与全局BA模块
- [ ] 添加三角化算法
- [ ] 添加全局BA算法

### CGraph管理模块

### 工具与辅助功能
- [ ] 添加View-Graph分割可视化工具
- [ ] 添加日志记录功能
- [ ] 编写单元测试

### 文档完善
- [ ] 编写使用示例
- [ ] 添加安装指南

## References

如果使用本项目进行研究，请引用原始 DAGSfM 项目及相关论文：

```bibtex
@article{chen2020graph,
  title={Graph-Based Parallel Large Scale Structure from Motion},
  author={Chen, Yu and Shen, Shuhan and Chen, Yisong and Wang, Guoping},
  journal={Pattern Recognition},
  pages={107537},
  year={2020},
  publisher={Elsevier}
}

@inproceedings{schoenberger2016sfm,
  author={Sch\"{o}nberger, Johannes Lutz and Frahm, Jan-Michael},
  title={Structure-from-Motion Revisited},
  booktitle={Conference on Computer Vision and Pattern Recognition (CVPR)},
  year={2016},
}
```

有关原始 DAGSfM 实现的更多信息，请访问: [https://github.com/AIBluefisher/DAGSfM](https://github.com/AIBluefisher/DAGSfM)