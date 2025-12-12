from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File    
import os
import tempfile
import pandas as pd
import warnings
import requests
from urllib.parse import urlparse


class Data():
    def download_from_sharepoint_old(self,site_url,file_url,new_filename,username,password):
        ctx_auth = AuthenticationContext(site_url)
        if ctx_auth.acquire_token_for_user(username, password):
            ctx = ClientContext(site_url, ctx_auth)
            with open(new_filename, 'wb') as output_file:
                file = (
                        ctx.web.get_file_by_server_relative_url(file_url).download(output_file).execute_query()
                )
            print("[Ok] file has been downloaded into: {0}".format(new_filename))    
    
    def get_access_token(self,clientID, clientSecret, tenantID):
        """
        Ottiene un token App-Only Azure AD v2 per Microsoft Graph
        """
        token_url = f"https://login.microsoftonline.com/{tenantID}/oauth2/v2.0/token"
        data = {
            "client_id": clientID,
            "client_secret": clientSecret,
            "scope": "https://graph.microsoft.com/.default",
            "grant_type": "client_credentials"
        }
        r = requests.post(token_url, data=data)
        r.raise_for_status()
        return r.json()["access_token"]

    def get_site_id(self,site_url, access_token):
        """
        Recupera il site_id da Microsoft Graph dato l'URL del sito
        """
        parsed = urlparse(site_url)
        hostname = parsed.netloc
        path = parsed.path.strip("/")  # es. 'sites/GBTS'
        graph_url = f"https://graph.microsoft.com/v1.0/sites/{hostname}:/{path}"
        headers = {"Authorization": f"Bearer {access_token}"}
        r = requests.get(graph_url, headers=headers)
        r.raise_for_status()
        return r.json()["id"]

    def download_from_sharepoint(self, site_url, file_path, new_filename, clientID, clientSecret, tenantID):
        """
        Scarica un file da SharePoint Online via Microsoft Graph API. clientSecret scade il 20/10/2027
        """
        try:
            # 1️⃣ Ottieni token
            access_token = self.get_access_token(clientID, clientSecret, tenantID)
            print("Token successfully obtained")

            # 2️⃣ Recupera site_id
            site_id = self.get_site_id(site_url, access_token)
            #print(f"Site ID obtained: {site_id}")

            # 3️⃣ Recupera tutti i drive del sito
            drives_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
            headers = {"Authorization": f"Bearer {access_token}"}
            drives_response = requests.get(drives_url, headers=headers)
            drives_response.raise_for_status()
            drives = drives_response.json()["value"]

            # 4️⃣ Trova il drive "Documents"
            documents_drive = next((d for d in drives if d["name"] == "Documents"), None)
            if not documents_drive:
                raise Exception("Drive 'Documents' not found in the site.")

            drive_id = documents_drive["id"]
            #print(f"Drive ID trovato: {drive_id}")

            # 5️⃣ URL di download del file
            graph_url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{file_path}:/content"
            #print(f"📥 Download da: {graph_url}")

            r = requests.get(graph_url, headers=headers, stream=True)
            #print(f"➡️ Status code: {r.status_code}")

            if r.status_code == 200:
                with open(new_filename, "wb") as f:
                    f.write(r.content)
                print(f"File downloaded: {new_filename}")
            else:
                print(f"Error {r.status_code}: {r.text[:300]}")

        except requests.HTTPError as e:
            print(f"HTTP Error: {e.response.status_code} {e.response.text}")
        except Exception as e:
            print(f"Error: {e}")

    def load_file(self, path: str, sheet: str):
        """Load data from an Excel file."""
        try:
            warnings.simplefilter(action='ignore', category=UserWarning)
            return pd.read_excel(path, sheet_name=sheet)
        except Exception as loadErr:
            print(loadErr)
            return pd.array([])