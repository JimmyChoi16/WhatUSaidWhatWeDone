# Backend – Flask Demo REST API

这是一个 **纯 REST API 的 Flask 后端 Demo 项目**，用于前后端分离开发演示。  
当前版本仅实现 **Demo 登录功能**，不接数据库、不做 JWT，但**代码结构已为后续扩展完整预留**。

---

## 一、项目特点

- 纯 REST API（无页面渲染）
- 前后端分离
- Demo 登录接口（固定密码）
- 使用 Python 虚拟环境（venv）
- 支持 Windows / macOS / Linux
- 结构清晰，可平滑升级

---

## 二、项目结构

```text
backend/
├── app/
│   ├── __init__.py          # 应用工厂（Flask 创建 / CORS / 注册蓝图）
│   ├── errors.py            # 全局错误处理（JSON）
│   ├── routes/
│   │   ├── health.py        # 健康检查接口
│   │   └── auth.py          # 登录接口（Demo + 预留）
│   └── models/
│       └── user.py          # User 模型占位（未启用）
├── config.py                # 配置（Demo + 预留）
├── requirements.txt         # Python 依赖
├── run.py                   # 启动入口
└── venv/                    # Python 虚拟环境（本地生成）
```

---

## 三、环境要求

- Python 3.9+
- Windows / macOS / Linux
- VS Code（推荐）
- PowerShell / CMD / Terminal

---

## 四、Windows 启动方式

### 1. 进入 backend 目录

```powershell
cd path\to\backend
```

### 2. 创建虚拟环境（仅第一次）

```powershell
python -m venv venv
```

### 3. 激活虚拟环境

#### PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

如果提示 **禁止运行脚本**：

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

关闭终端后重新打开，再执行激活命令。

#### CMD（备用）

```cmd
venv\Scripts\activate
```

成功后终端前会显示：

```text
(venv)
```

### 4. 安装依赖

```powershell
python -m pip install -r requirements.txt
```

### 5. 启动后端服务

```powershell
python run.py
```

---

## 五、macOS / Linux 启动方式

### 1. 进入 backend 目录

```bash
cd path/to/backend
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
```

### 3. 激活虚拟环境

```bash
source venv/bin/activate
```

### 4. 安装依赖

```bash
python -m pip install -r requirements.txt
```

### 5. 启动后端服务

```bash
python run.py
```

---

## 六、接口说明

### 1. 健康检查

**GET** `/api/health`

返回：

```json
{ "status": "ok" }
```

### 2. 登录接口（Demo）

**POST** `/api/auth/login`

请求体：

```json
{
  "username": "test",
  "password": "123"
}
```

成功返回：

```json
{
  "message": "login ok (demo)",
  "user": "test",
  "token": "demo-token-abc-123"
}
```

---

## 七、关于 404 的说明

本项目是 **纯 REST API**，未定义 `/` 首页。  
访问 `/` 返回 404 属于正常行为。

---

## 八、日志查看方式

所有日志直接输出在 **终端 / VS Code Terminal**。

---

## 九、配置说明（config.py）

```python
class Config:
    SECRET_KEY = "dev-secret-key"
    CORS_ORIGINS = "*"
    DEMO_PASSWORD = "123"
```

---

## 十、VS Code 说明

选择解释器：

```
Ctrl + Shift + P
→ Python: Select Interpreter
→ backend/venv/.../python.exe
```

---