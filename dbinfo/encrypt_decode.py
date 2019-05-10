import base64
from Crypto.Cipher import AES
# from crypto
class encrypt_and_decode:
    #秘钥
    def __init__(self):
        self.key = '@0yKGh%AGzwG0P*dXxj9!3ed2RSXz11E'
        self.vi  =  'OZ3sfNy7HxIkx5Vk'
        self.PADDING = '\0'

        # str不是16的倍数那就补足为16的倍数
    def add_to_16(self,textvalue):
        while len(textvalue) % 16 != 0:
            textvalue += '\0'
        return str.encode(textvalue)  # 返回bytes
    #加密
    def encrypted_text(self,text):
        try:
            keyvalue = self.key
            aes = AES.new(self.add_to_16(keyvalue),AES.MODE_ECB,self.vi)  # 初始化加密器
            encrypted_text = str(base64.encodebytes(aes.encrypt(self.add_to_16(text))), encoding='utf-8').replace('\n', '')  # 加密
            return encrypted_text
        except Exception  as e:
            return 'error value'

    #解密
    def decrypted_text(self,text):
        try:
            keyvalue = self.key
            aes = AES.new(self.add_to_16(keyvalue),AES.MODE_ECB,self.vi)  # 初始化加密器
            text_decrypted = str(
                aes.decrypt(base64.decodebytes(bytes(text, encoding='utf8'))).rstrip(b'\0').decode("utf8"))  # 解密
            return text_decrypted
        except Exception  as e:
            return 'error value'
#
# print(encrypt_and_decode().encrypted_text(''))
