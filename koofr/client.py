import requests
import posixpath
import os
import json

class KoofrClient:

    def __init__(self, api_base = "https://stage.koofr.net", verify_ssl = True):
        self.api_base = api_base
        self.S = requests.Session()

    def set_token(self, token):
        self._token = token
        self.S.headers['Authorization'] = 'Token ' + self._token

    def authenticate(self, email, password):
        resp = self.S.get(self.api_base + '/token', headers = {
            'X-Koofr-Email': email,
            'X-Koofr-Password': password
        })

        resp.raise_for_status()
        self.set_token(resp.headers['X-Koofr-Token'])
        return True

    def mounts(self):
        url = self.api_base + "/api/v2/mounts"
        resp = self.S.get(url)
        resp.raise_for_status()
        return resp.json()["mounts"]

    def files_get(self, mount_id, path):
        url = self.api_base + "/content/api/v2/mounts/" + mount_id + "/files/get"
        params = {'path': path}
        resp = self.S.get(url, params = params)
        resp.raise_for_status()
        return resp.content

    def files_get_to_path(self, mount_id, remote_path, local_path):
        url = self.api_base + "/content/api/v2/mounts/" + mount_id + "/files/get"
        params = {'path': remote_path}
        resp = self.S.get(url, params = params)

        with open(local_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
            f.flush()
            os.fsync(f)

    def files_put(self, mount_id, path, content):
        url = self.api_base + "/content/api/v2/mounts/" + mount_id + "/files/put"
        params = {'path': posixpath.dirname(path)}
        f = {'file': (posixpath.basename(path), content)}
        resp = self.S.post(url, params = params, files = f)
        resp.raise_for_status()
        return resp.json()[0]['name']

    def files_list(self, mount_id, path):
        url = self.api_base + "/api/v2/mounts/" + mount_id + "/files/list"
        params = {'path': path}
        resp = self.S.get(url, params = params)
        resp.raise_for_status()
        return resp.json()["files"]

    def files_info(self, mount_id, path):
        url = self.api_base + "/api/v2/mounts/" + mount_id + "/files/info"
        params = {'path': path}
        resp = self.S.get(url, params = params)
        return resp.json()

    def files_new_folder(self, mount_id, path):
        url = self.api_base + "/api/v2/mounts/" + mount_id + "/files/folder"
        params = {'path': posixpath.dirname(path)}
        data = {'name': posixpath.basename(path)}
        resp = self.S.post(url, params = params, data = json.dumps(data), headers = {'Content-Type': 'application/json'})
        resp.raise_for_status()
        return True

    def files_remove(self, mount_id, path):
        url = self.api_base + "/api/v2/mounts/" + mount_id + "/files/remove"
        params = {'path': path}
        resp = self.S.delete(url, params = params)
        resp.raise_for_status()
        return True
