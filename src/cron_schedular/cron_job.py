from apscheduler.schedulers.background import BackgroundScheduler
from functools import wraps

# 创建调度器
scheduler = BackgroundScheduler()

# 自定义装饰器
def cron_job(**cron_kwargs):
    def decorator(func):
        scheduler.add_job(func, 'cron', **cron_kwargs)
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

# ==============================
# 直接用 @cron_job 实现“注解”效果
# ==============================
@cron_job(hour=17, minute=47)  # 每天 0 点执行
def my_task():
    print("执行任务")

if __name__ == "__main__":
    scheduler.start()
    print("调度器已启动")
    import time
    try:
        while True:
            time.sleep(1)  # 保持程序运行
    except KeyboardInterrupt:
        scheduler.shutdown()
