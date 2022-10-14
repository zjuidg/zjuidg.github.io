## 资源修改
直接source文件夹内的资源与配置。

- intro.mp4

  小组介绍视频
  
- dict.json

  部分关键字的中英文切换词典（暂时只有英文）
  
- ycwu.json

  巫老师的资料
  
- students.json

  所有学生资料(*表示必须有)
  
  - *name：姓名
  - *photo：照片路径
  - startYear：在读生填写入学年份
  - *group：所在项目组
  - *title：头衔
  - *url：个人主页网址
  - degree：毕业生填写毕业学位
  - graduateYear：毕业生填写毕业年份
  - job：毕业生填写毕业去向
  
- publications.json

  论文列表
  
  - *id：简写名，尽量短，且可以作为网址的一部分
  - *title：论文标题
  - *teaser：teaser图
  - *DOI：DOI
  - *authors：作者列表
  - *source：投的期刊/会议名
  - *transaction：transaction全称
  - *year：年份
  - *abstract：摘要
  - volume：卷号
  - issue：题号
  - articleNo：文章序号
  - page：[开始页数，结束页数]
  - paper：论文pdf路径
  - video：视频网址
  - embedVideo：嵌入视频地址（一般按格式改一下就行）
  - demo：系统地址

  ```json
  {
    "title": "Towards Better Detection and Analysis of Massive Spatiotemporal Co-Occurrence Patterns",
    "DOI": "10.1109/TITS.2020.2983226",
    "authors": [
      "Yingcai Wu",
      "Di Weng",
      "Zikun Deng",
      "Jie Bao",
      "Mingliang Xu",
      "Zhangye Wang",
      "Yu Zheng",
      "Zhiyu Ding",
      "Wei Chen"
    ],
    "source": "TITS",
    "transaction": "IEEE Transactions on Intelligent Transportation Systems (TITS 2020)",
    "year": 2020,
    "abstract": "....",
    "video": "https://youtu.be/0T0xe-rppSo",
    "volume": 1,
    "issue": 1,
    "page": [1,16],
    "demo": "https://xxx.github.io"
  }
  ```

- featuredProj.json

  publication id列表

- updates.json

  最新公告
  
  - *date: 发布时间
  - *summary：内容
  - attachment：附件路径
  - link：跳转路径
  
- slides.json

  滚动图片
  
  - *title: 标题
  - subtitle：副标题
  - *imgSrc：图片路径
  - link：跳转路径
  
## 框架修改
请到[Gitlab](git.zjuidg.org/ZJUVIS/zjuidg_homepage)仓库修改React代码。
