# sprint0
# 目标
重构调用ai接口解析PDF的功能：对包含图片/表格的页面截图后调用 AI 接口转 Markdown

# 技术要求
使用glm-ocr能力，zai-sdk，如下

# 关键信息：api key：528b833ddafd74f7ce6d32f6d1e3b39e.yLrspX8jiUwh5BGd 需要从配置文件读取

# 安装最新版本
pip install zai-sdk
# 或指定版本
pip install zai-sdk==0.2.2
from zai import ZhipuAiClient

# 初始化客户端
client = ZhipuAiClient(api_key="your-api-key")

image_url = "https://cdn.bigmodel.cn/static/logo/introduction.png"

# 调用布局解析 API
response = client.layout_parsing.create(
    model="glm-ocr",
    file=image_url
)

# 输出结果
print(response)

详细文档：https://docs.bigmodel.cn/cn/guide/models/vlm/glm-ocr#python

先设计重构方案

## sprint1
重命名：nova-pdf 改成markitdown-glmocr
