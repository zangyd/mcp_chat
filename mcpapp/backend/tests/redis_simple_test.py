import redis

# 直接在代码中使用密码，避免命令行转义问题
redis_password = 'Redis@2024'

try:
    # 创建连接
    r = redis.Redis(
        host='8.130.142.155',
        port=6379,
        password=redis_password,
        decode_responses=True,
        socket_timeout=5
    )
    
    # 测试连接
    print("正在测试连接...")
    result = r.ping()
    print(f"连接测试结果: {result}")
    
except Exception as e:
    print(f"错误: {str(e)}")
    print(f"错误类型: {type(e).__name__}")
finally:
    try:
        r.close()
        print("连接已关闭")
    except:
        pass 