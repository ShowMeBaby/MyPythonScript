# 人脸识别结果对象
class result:
    def __init__(self, roll, pitch, yaw):
        self.roll = roll
        self.pitch = pitch
        self.yaw = yaw

    def __str__(self):
        return '{roll：%s,pitch：%s,yaw:%s}' % (self.roll, self.pitch, self.yaw)

    def serialize(self):
        return {'roll': self.roll, 'pitch': self.pitch, 'yaw': self.yaw}
