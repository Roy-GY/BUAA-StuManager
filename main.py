import subprocess
import sys 

def run_services():
    try:
        # 使用当前解释器启动 service.py
        service_process = subprocess.Popen([sys.executable, './server/service.py'])
        print("service.py is running...")

        # 使用当前解释器启动 app.py
        app_process = subprocess.Popen([sys.executable, './client/app.py'])
        print("app.py is running...")

        # Wait for both processes to complete
        service_process.wait()
        app_process.wait()
    except KeyboardInterrupt:
        print("Terminating processes...")
        service_process.terminate()
        app_process.terminate()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_services()
