
import asyncio
import os
import sys
import json

# 将当前目录加入路径以便导入
sys.path.append(os.getcwd())

# 模拟一些必要的全局对象和配置，防止导入报错
import utils.config as config
config.config = {
    "system": {
        "ignore_self_events": True,
        "enable_channel_event": False,
        "proxy": None,
        "started_text": "Started",
        "sync_guilds": []
    },
    "servers": []
}

import utils.message.v12.parser as parser
import utils.translator as translator
from utils.logger import get_logger

logger = get_logger("TestProtocol")

async def run_test():
    print("=== 开始协议兼容性本地测试 ===")
    
    # 测试案例 1：标准艾特
    test_case_1 = "<@1500149364927107183> 你好"
    # 测试案例 2：带感叹号的 Discord 艾特
    test_case_2 = "<@!1500149364927107183> 激活"
    # 测试案例 3：混合内容
    test_case_3 = "看这个 <@1500149364927107183> [图片]"
    
    cases = [test_case_1, test_case_2, test_case_3]
    
    for i, content in enumerate(cases):
        print(f"\n测试用例 {i+1}: {content}")
        
        # 1. 模拟 V12 分词与解析
        v12_msg = parser.parse_string(content)
        print(f"  [V12 消息段] {v12_msg}")
        
        # 2. 模拟事件包装
        dummy_event = {
            "post_type": "message",
            "detail_type": "group",
            "user_id": "123456",
            "message": v12_msg,
            "self": {"user_id": "1500149364927107183"}
        }
        
        # 3. 调用翻译器转换为 V11
        # 注意：translator 内部会修改 event 对象
        v11_event = dummy_event.copy()
        
        # 模拟 translator.py 里的翻译逻辑块
        v11_event["self_id"] = int(v11_event.pop("self")["user_id"])
        v11_event["message"] = await translator.translate_v12_message_to_v11(v11_event["message"])
        
        # 执行我们补全的 raw_message 生成逻辑
        raw_msg = ""
        for seg in v11_event["message"]:
            if seg["type"] == "text":
                text = str(seg["data"].get("text", ""))
                raw_msg += text.replace("&", "&amp;").replace("[", "&#91;").replace("]", "&#93;")
            else:
                items = list(seg["data"].items())
                if seg["type"] == "at" and "qq" in seg["data"]:
                    items.sort(key=lambda x: x[0] != "qq")
                data_str = ",".join(
                    f"{k}={str(v).replace('&', '&amp;').replace('[', '&#91;').replace(']', '&#93;').replace(',', '&#44;')}" 
                    for k, v in items
                )
                raw_msg += f"[CQ:{seg['type']},{data_str}]" if data_str else f"[CQ:{seg['type']}]"
        
        print(f"  [最终生成 RawMessage] {raw_msg}")
        
        # 验证断言
        if "1500149364927107183" in raw_msg and "[CQ:at,qq=" in raw_msg:
            print("  [结果] Success: Parse OK!")
        else:
            print("  [结果] Failed: Parse failed!")

if __name__ == "__main__":
    asyncio.run(run_test())
