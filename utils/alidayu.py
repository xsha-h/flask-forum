from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


class Alidayu(object):
    """
    api接口的初始化操作
    accessKeyId: api密钥的入口id
    accessSecret: api密钥的入口密码
    regionId: 一般是你云服务器的地区
    以上三个参数必不可少，封装成客户端实例
    发送配置（都是固定的配置）分别是发送短信的格式、域名、方式、协议、版本
    """
    def __init__(self):
        self.accessKeyId = "LTAI4FsNT1xcFWWHCGqyTpDW"
        self.accessSecret = "910uZ41GIX83zZ9n6B1Nh3Wgwo0UHh"
        self.regionId = "cn-shanghai"
        self.client = AcsClient(self.accessKeyId, self.accessSecret, self.regionId)

        # 发送配置（都是固定的配置）
        self.comRequest = CommonRequest()
        self.comRequest.set_accept_format("json")
        self.comRequest.set_domain("dysmsapi.aliyuncs.com")
        self.comRequest.set_method("POST")
        self.comRequest.set_protocol_type("https")
        self.comRequest.set_version("2017-05-25")

    def send_sms(self, telephone, code):
        """
        发送配置定义好，现在就是发送信息（验证码）
        发送信息之前的四个参数也是必不可少的：
        手机号码、短信签名名称、短信模板CODE、短信模板的内容参数值
        最后通过客户发送即可
        :param telephone: 手机号码
        :param code: 随机验证码
        :return:
        """
        self.comRequest.set_action_name("SendSms")
        self.comRequest.add_query_param("PhoneNumbers", telephone)
        self.comRequest.add_query_param("SignName", "校园论坛")
        self.comRequest.add_query_param("TemplateCode", "SMS_175475039")
        self.comRequest.add_query_param("TemplateParam", "{\"code\":\"%s\"}" % code)
        response = self.client.do_action(self.comRequest)
        print(response)
        return response
