"""
Unit tests for the features module
"""

import sys
import os

# Add the project root directory to the path so we can import dagsfm modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from dagsfm.features import FeatureExtractor, FeatureMatcher
from dagsfm.utils import create_database_file


def test_feature_extraction():
    """
    Test feature extraction with configured paths
    """
    print("Testing Feature Extraction")
    print("=" * 30)
    
    # 检查是否已配置路径
    if IMAGE_PATH == "/path/to/your/image.jpg":
        print("请先在文件顶部配置实际的图像路径！")
        return False
        
    if DATABASE_PATH == "/path/to/your/database.db":
        print("请先在文件顶部配置实际的数据库路径！")
        return False
    
    # 检查图像文件是否存在
    if not os.path.exists(IMAGE_PATH):
        print(f"错误：找不到图像文件 '{IMAGE_PATH}'")
        return False
    
    print(f"图像路径: {IMAGE_PATH}")
    print(f"数据库路径: {DATABASE_PATH}")
    
    try:
        # 创建数据库文件
        create_database_file(DATABASE_PATH)
        print(f"已创建数据库文件: {DATABASE_PATH}")
        
        # 创建特征提取器
        extractor = FeatureExtractor()
        
        # 执行特征提取
        print("正在执行特征提取...")
        result = extractor.extract_features(IMAGE_PATH, DATABASE_PATH)
        
        print("特征提取完成！")
        print(f"返回数据库路径: {result}")
        return True
        
    except NotImplementedError:
        print("特征提取功能尚未实现")
        return False
    except Exception as e:
        print(f"特征提取过程中发生错误: {e}")
        return False


def test_feature_matching():
    """
    Test feature matching with configured database path
    """
    print("\nTesting Feature Matching")
    print("=" * 30)
    
    # 检查是否已配置路径
    if DATABASE_PATH == "/path/to/your/database.db":
        print("请先在文件顶部配置实际的数据库路径！")
        return False
    
    # 检查数据库文件是否存在
    if not os.path.exists(DATABASE_PATH):
        print(f"错误：找不到数据库文件 '{DATABASE_PATH}'")
        print("请先运行特征提取测试以创建数据库文件")
        return False
    
    print(f"数据库路径: {DATABASE_PATH}")
    
    try:
        # 创建特征匹配器
        matcher = FeatureMatcher()
        
        # 执行特征匹配
        print("正在执行特征匹配...")
        result = matcher.exhaustive_matcher(DATABASE_PATH)
        result = matcher.spatial_matcher(DATABASE_PATH)
        
        print("特征匹配完成！")
        print(f"返回数据库路径: {result}")
        return True
        
    except NotImplementedError:
        print("特征匹配功能尚未实现")
        return False
    except Exception as e:
        print(f"特征匹配过程中发生错误: {e}")
        return False


def test_full_pipeline():
    """
    Test full pipeline: feature extraction followed by feature matching
    """
    print("\nTesting Full Pipeline")
    print("=" * 30)
    
    extraction_success = test_feature_extraction()
    if not extraction_success:
        print("特征提取失败，无法继续执行完整流水线测试")
        return False
    
    matching_success = test_feature_matching()
    return matching_success


if __name__ == "__main__":
    # 配置真实测试路径 - 请在这里修改为您实际的路径
    IMAGE_PATH = "/ws/18_nfs/zwl/Data/DJI/jimeimigu/images"      # 修改为您的实际图像路径
    DATABASE_PATH = "/ws/18_nfs/zwl/Data/DJI/jimeimigu/database_dagsfm_python.db" # 修改为您的实际数据库路径
    
    print("选择要运行的测试:")
    print("1. 仅测试特征提取")
    print("2. 仅测试特征匹配")
    print("3. 测试完整流水线(特征提取+特征匹配)")
    
    choice = input("请输入选项 (1/2/3, 默认为1): ").strip()
    
    if choice == "2":
        test_feature_matching()
    elif choice == "3":
        test_full_pipeline()
    else:
        test_feature_extraction()