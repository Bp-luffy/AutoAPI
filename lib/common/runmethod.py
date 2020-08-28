# coding=utf-8
import requests


class runMethod():
    def post_main(self, url, data, header=None):
        res = None
        if header != None:
            res = requests.post(url=url, data=data, headers=header)
        else:
            res = requests.post(url=url, data=data)
        return res

    def get_main(self, url, data=None, header=None):
        res = None
        if header != None:
            res = requests.get(url=url, params=data, headers=header)
        else:
            res = requests.get(url=url, params=data)
        return res

    def run_main(self, method, url, data=None, header=None):
        res = None
        if method == 'Post':
            res = self.post_main(url, data, header)
        else:
            res = self.get_main(url, data, header)
        return res


if __name__ == '__main__':
    url = "http://132.232.179.210:32154/f?bid=H8QSHENSQJ42&action=62&param=hxpvNx-ViU5Yh2A8nEZmjSpAq0syLzzDxmtM6MSJQ_TGqNYji8_dTfrFvWjNyP0cyGXGtalbK65dMGlvTNt6zu7g47ksl0Y5b2OMW4tlLNS2WCfNz4hXmzwlbbBdhUVR&url=https://baidu.com&title=titletest01"
    data = {
        'param': 'hxpvNx-ViU5Yh2A8nEZmjSpAq0syLzzDxmtM6MSJQ_TGqNYji8_dTfrFvWjNyP0cyGXGtalbK65dMGlvTNt6zu7g47ksl0Y5b2OMW4tlLNS2WCfNz4hXmzwlbbBdhUVR',
        'bid': 'H8QSHENSQJ42', 'action': 23}
    r = runMethod().run_main('get', url, data)
    print(r.status_code)
