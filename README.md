# FastAPI + Vue 3

## 环境准备

### pyenv
#### pyenv 安装指南

[pyenv](https://github.com/pyenv/pyenv) 是一个简单、强大的 Python 版本管理工具，允许你在同一系统上安装和切换多个 Python 版本。

##### macOS 安装

在 macOS 上，可以使用 Homebrew 安装 pyenv：

```bash
brew update
brew install pyenv
```

然后将以下内容添加到你的 shell 配置文件（如 ~/.zshrc 或 ~/.bash_profile）：

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

##### Windows 安装

Windows 用户可以使用 pyenv-win：

1. 使用 PowerShell 安装：

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

2. 或使用 Git 安装：

```bash
git clone https://github.com/pyenv-win/pyenv-win.git "$HOME/.pyenv"
```

安装后，将以下路径添加到环境变量：
- `%USERPROFILE%\.pyenv\pyenv-win\bin`
- `%USERPROFILE%\.pyenv\pyenv-win\shims`

### pdm 安装指南

[pdm](https://pdm.fasterpython.com/) 是一个快速的 Python 包管理工具，用于替代 pip、venv 等工具。

#### pdm 安装指南

##### macOS 安装

在 macOS 上，可以使用 Homebrew 安装 pdm：

```bash
brew install pdm
```

##### Windows 安装

Windows 用户可以使用 pip 安装 pdm：

```bash
pip install pdm
```

### Bun 安装指南

[Bun](https://bun.sh/) 是一个快速的 JavaScript 运行时、包管理器和打包工具，可用于替代 Node.js、npm、webpack 等工具。以下是在不同操作系统上安装 Bun 的指南。

### macOS 安装

在 macOS 上，你可以使用以下几种方法安装 Bun：

#### 使用 curl（推荐）

```bash
curl -fsSL https://bun.sh/install | bash
```

#### 使用 Homebrew

```bash
brew tap oven-sh/bun
brew install bun
```

#### 使用 npm

```bash
npm install -g bun
```

### Windows 安装

Bun 在 Windows 上的支持已经稳定。以下是在 Windows 上安装 Bun 的方法：

#### 使用 PowerShell（推荐）

```powershell
powershell -c "irm bun.sh/install.ps1 | iex"
```

#### 使用 npm

```bash
npm install -g bun
```

#### 使用 scoop

```bash
scoop install bun
```

#### 使用 Windows Subsystem for Linux (WSL)

如果你使用 WSL，可以按照 macOS/Linux 的安装方法进行安装：

```bash
curl -fsSL https://bun.sh/install | bash
```

### 验证安装

安装完成后，可以通过以下命令验证 Bun 是否安装成功：

```bash
bun --version
```

### 更新 Bun

要更新到最新版本的 Bun，可以使用以下命令：

```bash
bun upgrade
```

### 使用 Bun 替代 npm

可以使用 Bun 替代 npm 来管理包和运行脚本：

```bash
# 安装依赖
bun install

# 添加依赖
bun add [package]

# 运行脚本
bun run [script]

# 执行 JavaScript 文件
bun [file.js]
```

## 项目介绍

