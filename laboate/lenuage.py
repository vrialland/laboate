import urequests


class LeNuage:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def _get_tiles_url(self):
        return '{}/boites/{}/'.format(self.base_url.rstrip('/'),
                                      self.api_key)

    def _get_tile_url(self, tile_id):
        return '{}/boites/{}/tiles/{}/'.format(self.base_url.rstrip('/'),
                                               self.api_key,
                                               tile_id)

    def get_tiles(self):
        url = self._get_tiles_url()
        print('GET {}'.format(url))
        response = urequests.get(url)
        json = response.json()
        response.close()
        return json

    def get_tile(self, tile_id):
        url = self._get_tile_url(tile_id)
        print('GET {}'.format(url))
        response = urequests.get(url)
        json = response.json()
        response.close()
        return json
