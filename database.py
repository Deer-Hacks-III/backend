import requests
API_URL = "http://172.17.195.155:5000"


class Database:

    def get_upc(self, upc: str):
        data = {'upc': upc}
        r = requests.get(f'{API_URL}/list/{upc}')
        return r.json()

    def add_upc(self, upc: str):
        r = requests.post(f'{API_URL}/list/{upc}')
        return r.json()
    

if __name__ == "__main__":
    base = Database()
    print(base.get_upc('3045140105502'))
