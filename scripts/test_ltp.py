import sys
from ltp import LTP

def test_ltp():
    try:
        print(f"Python 版本: {sys.version}")
        
        # 1. 初始化模型 (会自动下载小型权重文件)
        # 注意：如果是首次运行，确保网络通畅
        ltp = LTP() 
        
        # 2. 执行分词和命名实体识别
        test_text = "他叫张三，在哈尔滨工业大学就读。"
        result = ltp.pipeline([test_text], tasks=["cws", "pos", "ner"])
        
        # 3. 检查输出
        print("\n--- 测试成功 ---")
        print(f"分词: {result.cws}")
        print(f"词性: {result.pos}")
        print(f"实体: {result.ner}")
        
        return True
    except Exception as e:
        print("\n--- 测试失败 ---")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {e}")
        return False

if __name__ == "__main__":
    test_ltp()