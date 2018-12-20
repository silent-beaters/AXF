import oss2

NON_PAYMENT = 1
HAVE_PAID = 2
NOT_YET_SHIPPED = 3
SHIPPED = 4
REMAIN_TO_BE_EVALUATED = 5
HAVE_EVALUATION = 6
COMPLETED = 0


def upfile1(imgKey, imgPath):
    auth = oss2.Auth('LTAI1u1akA1rfZQy', 'Qw99cfuozCA1XTDTJhTqzTYBEmDtPD')
    bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', '1813axf')
    bucket.put_object_from_file(imgKey, imgPath)
    style = 'image/resize,m_fixed,w_200,h_200'
    url = bucket.sign_url('GET', imgKey, 300 * 24 * 60 * 60, params={'x-oss-process': style})
    return url
def upfile2(imgKey, imgBytes):
    auth = oss2.Auth('LTAI1u1akA1rfZQy', 'Qw99cfuozCA1XTDTJhTqzTYBEmDtPD')
    bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', '1813axf')
    bucket.put_object(imgKey, imgBytes)
    style = 'image/resize,m_fixed,w_200,h_200'
    url = bucket.sign_url('GET', imgKey, 300 * 24 * 60 * 60, params={'x-oss-process': style})
    return url