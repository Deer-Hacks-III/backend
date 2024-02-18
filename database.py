import requests
API_URL = "127.0.0.1:8324"


class Database:

    def get_upc(self, upc: str):
        data = {'upc': upc}
        r = requests.get(f'{API_URL}/list', json=data)
        return r.json()


if __name__ == "__main__":
    base = Database()
    print(base.get_upc('3045140105502'))
