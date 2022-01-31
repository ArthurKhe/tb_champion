import requests


class Requester:
    def requesting(self, url, pk=""):
        try:
            res = requests.get(url + pk)
            if res:
                data = res.json()
                return data
            else:
                return 0
        except Exception as ex:
            return ex
