import uaiohttpclient as aiohttp
import ujson as json


class LeNuage:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self._tiles_cache = {}

    def _get_tiles_url(self):
        return '{}/boites/{}/'.format(self.base_url.rstrip('/'),
                                      self.api_key)

    def _get_tile_url(self, tile_id):
        return '{}/boites/{}/tiles/{}/'.format(self.base_url.rstrip('/'),
                                               self.api_key,
                                               tile_id)

    async def _get_response_json(self, response):
        text = await response.read()
        return json.loads(text)

    async def get_tiles(self):
        url = self._get_tiles_url()
        print('GET {}'.format(url))
        response = await aiohttp.request('GET', url)
        json = await self._get_response_json(response)
        # Cache tiles' id and last_activity
        for tile in json['tiles']:
            tile_id = tile['id']
            if tile_id not in self._tiles_cache:
                # Tile is not known yet
                self._tiles_cache[tile_id] = {
                    'last_activity': tile['last_activity'],
                    'update_needed': True,
                    'data': None
                }
            else:
                cache = self._tiles_cache[tile_id]
                if tile['last_activity'] != cache['last_activity']:
                    # Tile needs update
                    cache['last_activity'] = tile['last_activity']
                    cache['update_needed'] = True
        return json

    async def get_tile(self, tile_id):
        cache = self._tiles_cache.get(tile_id)
        if not cache or cache['update_needed']:
            # No cache set or tile needs refresh
            url = self._get_tile_url(tile_id)
            print('Get tile {} data from {}'.format(tile_id, url))
            response = await aiohttp.request('GET', url)
            json = await self._get_response_json(response)
            cache['data'] = json
            cache['update_needed'] = False
            data = json
        else:
            # Get data from cache
            print('Get tile {} data from cache'.format(tile_id))
            data = cache['data']
        return data
