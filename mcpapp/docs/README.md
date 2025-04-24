# MCP Server 智能聊天系统

基于Vue3和Python的智能聊天系统，支持与DeepSeek大模型交互，并能自动选择合适的MCP Server提供服务。

## 快速开始

### 后端服务

1. 安装依赖
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，配置必要的环境变量
```

3. 初始化数据库
```bash
alembic upgrade head
```

4. 启动服务
```bash
uvicorn main:app --reload
```

### 前端服务

1. 安装依赖
```bash
cd frontend
npm install
```

2. 启动开发服务器
```bash
npm run dev
```

3. 构建生产版本
```bash
npm run build
```

## 项目文档

- [技术架构文档](./docs/ARCHITECTURE.md)
- [API文档](http://localhost:8000/docs)
- [开发指南](./docs/development.md)
- [部署指南](./docs/deployment.md)

## 开发规范

请参考[开发规范文档](./docs/coding-standards.md)进行开发。

## 测试

### 后端测试
```bash
cd backend
pytest
```

### 前端测试
```bash
cd frontend
npm run test
```

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件