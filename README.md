# DAGSfM-Python

DAGSfM-Python是一个基于Python的Structure from Motion (SfM)系统，采用有向无环图(DAG)方法优化三维重建过程。该项目利用图论中的N-cut算法对场景进行分割，然后并行处理各个子块，最后合并结果以获得完整的三维重建。

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

### 1. 特征提取与匹配模块 ([features.py](file:///ws/zwl/Code/SfM/DAGSfM-Python/dagsfm/features.py))
负责从图像中提取特征点（如SIFT、SURF等）并进行特征匹配，构建图像间的匹配关系图。

### 2. 场景分块模块 ([partition.py](file:///ws/zwl/Code/SfM/DAGSfM-Python/dagsfm/partition.py))
基于N-cut算法对整个场景进行分割，将大型SfM问题分解为多个较小的子问题。该模块包含：
- ViewGraphNode类：表示图像节点
- ViewGraph类：管理视图图结构
- NcutPartitioner类：实现N-cut分割算法

### 3. 子块重建模块 ([reconstruction.py](file:///ws/zwl/Code/SfM/DAGSfM-Python/dagsfm/reconstruction.py))
使用pycolmap或colmap对分割后的子块进行独立重建。

### 4. 子块合并与BA模块 ([merging.py](file:///ws/zwl/Code/SfM/DAGSfM-Python/dagsfm/merging.py))
将各个子块的重建结果进行配准和合并，并进行全局光束法平差(Bundle Adjustment)优化。

### 5. 工作流管理模块 ([pipeline.py](file:///ws/zwl/Code/SfM/DAGSfM-Python/dagsfm/pipeline.py))
使用CGraph的Python版本管理系统整体工作流程和模块间依赖关系。

## 测试

本项目为每个模块都提供了单元测试。可以通过以下方式运行测试：

```bash
# 运行所有测试
python run_tests.py

# 或者使用unittest模块运行测试
python -m unittest discover tests/
```

测试文件说明：
- [test_features.py](file:///ws/zwl/Code/SfM/DAGSfM-Python/tests/test_features.py): 测试特征提取与匹配模块
- [test_partition.py](file:///ws/zwl/Code/SfM/DAGSfM-Python/tests/test_partition.py): 测试场景分块模块
- [test_reconstruction.py](file:///ws/zwl/Code/SfM/DAGSfM-Python/tests/test_reconstruction.py): 测试子块重建模块
- [test_merging.py](file:///ws/zwl/Code/SfM/DAGSfM-Python/tests/test_merging.py): 测试子块合并与BA模块
- [test_pipeline.py](file:///ws/zwl/Code/SfM/DAGSfM-Python/tests/test_pipeline.py): 测试工作流管理模块
- [test_utils.py](file:///ws/zwl/Code/SfM/DAGSfM-Python/tests/test_utils.py): 测试工具函数模块

## 设计模式选择

本项目采用了以下几种设计模式来保证系统的可扩展性和可维护性：

### 1. 模块化设计模式
将系统划分为多个功能独立的模块，每个模块负责特定的功能，降低了系统复杂度，提高了代码复用性。

### 2. 工厂模式
在特征提取等模块中，根据不同需求创建不同的特征提取器（如SIFT、SURF等），便于扩展新的特征提取算法。

### 3. 策略模式
在重建模块中，可以选择使用pycolmap或colmap进行重建，通过策略模式可以方便地切换不同的实现。

### 4. 观察者模式
在工作流管理中，通过CGraph实现任务节点间的依赖管理，当某个任务完成时，自动触发后续依赖任务的执行。

## TODO List

### 核心框架开发
- [✔] 根据viewgraph对场景使用Ncut算法进行分割与扩展
- [ ] 设计图像节点表示类
- [ ] 实现节点间边的关系定义
- [ ] 添加DAG构建和管理功能

### 特征提取与匹配模块
- [ ] 集成OpenCV特征提取算法(SIFT, SURF等)
- [ ] 实现特征匹配功能
- [ ] 添加特征匹配优化算法
- [ ] 构建图像间匹配关系图

### SfM核心算法实现
- [ ] 相机模型初始化
- [ ] 实现基础的三角化算法
- [ ] 添加BA(Bundle Adjustment)优化模块
- [ ] 实现增量式SfM流程

### DAG调度与分布式处理
- [ ] 设计子任务划分算法
- [ ] 实现基于DAG的任务调度器
- [ ] 添加并行处理支持
- [ ] 实现子网对齐与融合算法

### 工具与辅助功能
- [ ] 添加点云可视化工具
- [ ] 实现相机轨迹可视化
- [ ] 添加日志记录功能
- [ ] 编写单元测试

### 文档完善
- [ ] 补充项目详细说明
- [ ] 添加API文档
- [ ] 编写使用示例
- [ ] 添加安装指南