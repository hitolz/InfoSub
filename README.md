# InfoSub

## 什么是 InfoSub

InfoSub 是一个信息聚合工具, 支持将网站、 微信公众号等各种资讯网站统一聚合, 并为用户提供自定义订阅服务。


## 技术栈

信息聚合主要使用 RSS, 爬虫, 因此技术栈是:

  - Python 2.7 (日后升级为 3.6
  - Flask
  - Celery
  - Scrapy

## 搭建

### 安装依赖

```
pip install -r requirements.txt
```

### 运行

按照 `config.py` 配置环境变量

```
python manage.py runserver
```

#### 初始化数据库

```
python manage.py initdb
```


