#!/usr/bin/env python3
"""
测试main.py的运行情况
"""
import sys
import traceback

try:
    print("开始导入main模块...")
    import main
    print("main模块导入成功")
    
    print("开始运行main函数...")
    main.main()
    print("main函数执行完毕")
    
except Exception as e:
    print(f"捕获到异常: {e}")
    print("详细错误信息:")
    traceback.print_exc()
except KeyboardInterrupt:
    print("用户中断程序")
except SystemExit as e:
    print(f"程序退出，退出代码: {e.code}")
finally:
    print("测试完成") 