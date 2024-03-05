import requests

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str):
        """Метод загруджает файл file_path на Яндекс.Диск"""
        headers = {'Authorization': self.token, 'Accept': 'application/json'}
        # upl_dir = urllib.parse.quote('/Dobroe, staroe vremja.txt')
        # в документации API по загрузке пишут, что создаваевый путь на диске должен быть закодирован в URL-формате; в итоге всё и так работает - какого?
        upl_dir = '/Dobroe, staroe vremja.txt'
        host_url = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload'
        params = {'path': upl_dir, 'overwrite': 'true'}
        get_upload_url = requests.get(host_url, params=params, headers=headers)
        upl_obj = get_upload_url.json()
        url_text = upl_obj['href']
        with open(file_path, 'rb') as poem:
            upl_file = requests.put(url_text, files={'file': poem})
        print(upl_file)
        return 'Файл успешно загружен на Диск'