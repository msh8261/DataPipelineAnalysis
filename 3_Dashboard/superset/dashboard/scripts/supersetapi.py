import requests
import json

class SupersetAPIClient:
    
    def __init__(self, host):
        self.base_url = host + "/api/v1"
        self.access_token = ""
        self.session = requests.session()
        self.session.headers["Referer"] = self.base_url

    def login(self, username, password):
        payload = {
            "username": username,
            "password": password,
            "provider": "db"
        }
        payload_json = json.dumps(payload)
        headers = {'Content-Type': 'application/json'}
        res = self.session.post(url=self.base_url + "/security/login", data=payload_json,
                            verify=False, headers=headers)
        res.raise_for_status()
        print(f"Superset loggin Status Code: {res.status_code}")
        self.access_token = res.json()['access_token']

        # Construct the Authorization header of the form Bearer access_token
        headers = {'Authorization': 'Bearer ' + self.access_token}
        res1 = self.session.get(self.base_url + '/security/csrf_token', 
                                verify=False, headers=headers)
        res1.raise_for_status()
        print(f"Superset csrf_token Status Code: {res1.status_code}")
        self.csrf_token = res1.json()['result']

        self.session.headers['X-CSRFToken'] = self.csrf_token
        self.session.headers['Authorization'] = 'Bearer ' + self.access_token
        self.session.headers['Content-Type'] = 'application/json'

    
    def create_database(self, database_name, driver, engine, sqlalchemy_uri):
        payload = {
                    "configuration_method": "sqlalchemy_form",
                    "database_name": database_name,
                    "driver": driver,
                    "engine": engine,
                    "sqlalchemy_uri": sqlalchemy_uri,

                }
        payload_json = json.dumps(payload)

        res = self.session.post(url=f"{self.base_url}/database", data=payload_json, verify=False)
        print(res.text)
        res.raise_for_status()
        print(f"Superset database Status Code: {res.status_code}")
        database_id = res.json()['id']
        return database_id
        

    def create_dataset(self, database_id, schema, table):
        payload = {
            "database": database_id,
            "schema": schema,
            "table_name": table
        }
        payload_json = json.dumps(payload)

        r = self.session.post(url=self.base_url + "/dataset", data=payload_json, verify=False)
        r.raise_for_status()
        print(f"Superset dataset Status Code: {r.status_code}")
        dataset_id = r.json()['id']
        return dataset_id
    
    def create_dashboard(self, title):
        payload = {
            "dashboard_title": title
        }
        payload_json = json.dumps(payload)

        r = self.session.post(url=self.base_url + "/dashboard", data=payload_json, verify=False)
        r.raise_for_status()
        print(f"Superset dashboard Status Code: {r.status_code}")
        dashboard_id = r.json()['id']
        return dashboard_id
    
    def create_chart(self, dashboard_ids: list, datasource_id:int, datasource_name:str, params:str, slice_name:str, viz_type:str):
        payload = {
            "dashboards": dashboard_ids,
            "datasource_id": datasource_id,
            "datasource_name": datasource_name,
            "datasource_type": "table",
            "params": params,
            "slice_name": slice_name,
            "viz_type": viz_type
        }
        payload_json = json.dumps(payload)

        r = self.session.post(url=self.base_url + "/chart", data=payload_json, verify=False)
        r.raise_for_status()
        print(f"Superset chart Status Code: {r.status_code}")
        chart_id = r.json()['id']
        return chart_id
