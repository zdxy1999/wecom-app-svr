FROM docker.xuanyuan.me/panzhongxian/wecom-bot-svr

# 安装最新版本的 wecom-app-svr 包
RUN python3 -m pip install wecom-app-svr==0.1.0

# 安装额外依赖
RUN python3 -m pip install \
    python-dotenv \
    requests \
    apscheduler

# 复制项目文件
COPY adapter.py /data/code/
COPY .env /data/code/

# 复制 cron_schedular 模块（从项目根目录的 src 复制）
COPY ../src/cron_schedular /data/code/cron_schedular/

# 设置工作目录
WORKDIR /data/code

# 设置 Python 路径
ENV PYTHONPATH=/data/code

# 暴露端口
EXPOSE 8080

# 启动命令
CMD ["python3", "/data/code/adapter.py"]
