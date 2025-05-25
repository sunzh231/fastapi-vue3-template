# 使用官方的 Python 基础映像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV BUN_INSTALL="/root/.bun"
ENV PATH="${BUN_INSTALL}/bin:${PATH}"

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 安装 Bun
RUN apt-get update && apt-get install -y curl unzip && \
    curl -fsSL https://bun.sh/install | bash && \
    ln -s ${BUN_INSTALL}/bin/bun /usr/local/bin/bun && \
    ln -s ${BUN_INSTALL}/bin/bunx /usr/local/bin/bunx

# 将项目源代码复制到工作目录
COPY . .

# 安装后端依赖项
RUN uv sync --frozen --no-cache

# 安装前端依赖项并构建前端代码
RUN bun install && bun run build

# 暴露容器运行时的端口
EXPOSE 8000

# 启动 fastapi 应用
CMD ["/app/.venv/bin/fastapi", "run", "main.py", "--port", "8000", "--host", "0.0.0.0"]
