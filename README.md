# InfoSub

## 什么是 InfoSub

InfoSub 是一个信息聚合工具, 支持将网站、 微信公众号等各种资讯网站统一聚合, 并为用户提供自定义订阅服务。


## 技术栈

信息聚合主要使用 RSS, 爬虫, 因此技术栈是:

  - Python 2.7 (日后升级为 3.6
  - Flask
  - Celery
  - Scrapy

## 开发准备

### 安装依赖

建议在安装依赖前创建并使用虚拟环境。

```
pip install -r requirements.txt
```

### 运行

首先需要配置数据库并按照 `config.py` 配置环境变量

#### 启动服务

```
python manage.py runserver
```

#### 初始化数据库

```
python manage.py initdb
```

## 部署

Docker, Of Course

### STEP 1. 启动服务

```
docker-compose -f docker-compose.yml up -d
```

### STEP 2. 初始化数据库

```
docker-compose -f docker-compose.yml exec sub_service python manage.py initdb
```

然后可以访问 http://127.0.0.1 即可, 默认管理员: `admin`, 登录密码: `admin`

**线上一定不要使用 yml 里的默认密码**

