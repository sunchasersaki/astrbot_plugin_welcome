import astrbot.api.message_components as Comp
from astrbot.api import logger
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter
from astrbot.core import AstrBotConfig

# ▽▽▽ 你只需要修改下面这3个变量即可 ▽▽▽
TARGET_GROUP_ID = "1044962036"
WELCOME_TEXT = (
    "欢迎老师来到安安生日会游客群！\n"
    "请老师先阅读群公告，有问题请私信群管理。\n"
    "北京夏目安安生日会即将开启！请老师敬请期待，也祝老师在群里玩得愉快！"
)
WELCOME_IMAGE_PATH = "data/welcome.jpg"   # 建议图片放在 data/ 目录下并用这个文件名

@register(
    "astrbot_plugin_welcome",
    "自动欢迎插件",
    "新成员进群自动@+发送文字+图片混合欢迎",
    "v1.1",
)
class WelcomeOnlyPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig = None):
        super().__init__(context)
        self.config = config or {}

        # 可通过config覆盖默认设置（非必须）
        self.target_group_id = str(self.config.get("target_group_id", TARGET_GROUP_ID))
        self.welcome_text = self.config.get("welcome_text", WELCOME_TEXT)
        self.welcome_image_path = self.config.get("welcome_image_path", WELCOME_IMAGE_PATH)

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def handle_group_increase(self, event):
        """新成员入群时自动@+发送文字+图片欢迎（无禁言/权限限制）"""
        try:
            raw = getattr(event.message_obj, "raw_message", {})
            if (
                raw.get("post_type") == "notice"
                and raw.get("notice_type") == "group_increase"
            ):
                group_id = str(raw.get("group_id", ""))
                user_id = int(raw.get("user_id", 0))

                if group_id != self.target_group_id:
                    return

                msg_chain = [
                    Comp.At(qq=user_id),
                    Comp.Plain(text=self.welcome_text),
                    Comp.Image(file=f"file:///{self.welcome_image_path}")
                ]
                yield event.chain_result(msg_chain)
        except Exception as e:
            logger.error(f"发送自动欢迎消息出错: {e}")
