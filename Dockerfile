FROM python:3.12-slim as backend

WORKDIR /app

# 安装PDM和项目依赖
RUN pip install --no-cache-dir pdm
COPY pyproject.toml pdm.lock ./
RUN pdm install --prod --no-lock --no-editable

# 复制后端代码
COPY app ./app
COPY main.py ./

# 从Node.js镜像构建前端
FROM oven/bun:1 as frontend

WORKDIR /app

# 复制前端相关文件
COPY package.json bun.lockb ./
COPY index.html vite.config.js ./
COPY frontend ./frontend
COPY public ./public

# 安装依赖并构建前端
RUN bun install
RUN bun run build

# 最终镜像
FROM python:3.12-slim

WORKDIR /app

# 安装运行时依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# 从backend阶段复制Python环境和代码
COPY --from=backend /app /app
COPY --from=backend /root/.local/share/pdm /root/.local/share/pdm
ENV PATH="/root/.local/share/pdm/venv/bin:$PATH"

# 从frontend阶段复制构建好的前端文件
COPY --from=frontend /app/templates ./templates
COPY --from=frontend /app/templates/assets ./assets

# 暴露端口
EXPOSE 8000

# 启动应用
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
