import subprocess
import time
import os

# --- 配置区 ---
LOG_FILE = "/root/agora/agora_output_gpu0.log"
START_CMD = ["python3", "agora_cli.py", "start", "--skip_input"]
CHECK_INTERVAL = 2.0 

def run_start():
    print(f"[{time.ctime()}] 正在尝试启动 Agora...")
    try:
        # 使用 Popen 而不是 run，确保我们不会阻塞监控逻辑
        subprocess.Popen(START_CMD)
    except Exception as e:
        print(f"启动失败: {e}")

def get_last_line(filepath):
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return ""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            return lines[-1].strip() if lines else ""
    except Exception:
        return ""

def monitor():
    print(f"[{time.ctime()}] 开始监控日志: {LOG_FILE}")
    
    while True:
        last_line = get_last_line(LOG_FILE)
        
        # 调试用：查看当前读取到的最后一行是什么
        # print(f"DEBUG: {last_line}") 

        # 核心判断逻辑
        if "Shutting down" in last_line or "[ERROR]" in last_line:
            print(f"[{time.ctime()}] 检测到服务已关闭，准备重启...")
            run_start()
            # 启动后等待一段时间，让新日志生成，避免瞬时重复触发
            time.sleep(60) 
        
        elif not last_line:
            print(f"[{time.ctime()}] 日志为空或不存在，尝试初始化启动...")
            run_start()
            time.sleep(60)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor()
