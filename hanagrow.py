import os
import requests
import json
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)

def refresh_access_token(refresh_token):
    api_key = os.getenv("API_KEY")
    url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    headers = {
        "Content-Type": "application/json",
    }

    body = json.dumps({
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    })

    response = requests.post(url, headers=headers, data=body)
    
    logging.info(f"Token refresh response: {response.json()}")
    
    if response.status_code != 200:
        error_response = response.json()
        raise Exception(f"Failed to refresh access token: {error_response.get('error', 'Unknown error')}")

    return response.json()

def print_intro():
    print("Auto Grow for HANA Network")

def print_success(message):
    print(message)

def print_error(message):
    print(message)

def execute_graphql_query(session, url, headers, query, variables=None):
    response = session.post(url, headers=headers, json={"query": query, "variables": variables})
    if response.status_code == 401:  
        return None, response.json() 
    elif response.status_code != 200:
        logging.error(f"Failed request with response: {response.json()}")
        return None, response.json()
    return response.json(), None

def main():
    refresh_token = os.getenv("REFRESH_TOKEN")
    proxy = os.getenv("PROXY_URL")

    if not refresh_token:
        print_error("Refresh token not found in environment variables.")
        return

    print("Input Grow Amount: ")
    try:
        num_iterations = int(input())
        if num_iterations <= 0:
            raise ValueError("The number of iterations must be a positive integer.")
    except ValueError as e:
        logging.error(f"Invalid input: {e}")
        print_error("Input not valid.")
        exit()

    while True:
        try:
            session = requests.Session()
            if proxy:
                session.proxies = {
                    "http": proxy,
                    "https": proxy,
                }
                logging.info(f"Connected to proxy: {proxy}")
                print_success(f"Proxy connected: {proxy}")

            token_data = refresh_access_token(refresh_token)
            access_token = token_data.get("access_token")

            url = "https://hanafuda-backend-app-520478841386.us-central1.run.app/graphql"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            }

            for i in range(num_iterations):
                query_get_top_status_snapshots = """
                query getTopStatusSnapshots($offset: Int, $limit: Int) {
                    getTopStatusSnapshots(offset: $offset, limit: $limit) {
                        user {
                            id
                            name
                        }
                    }
                }
                """
                variables_top_status = {"offset": 0, "limit": 100}
                result, error = execute_graphql_query(session, url, headers, query_get_top_status_snapshots, variables_top_status)

                if error:  
                    if 'errors' in error and 'UNAUTHORIZED' in error['errors'][0]['message']:
                        logging.info("Access token expired, refreshing token...")
                        token_data = refresh_access_token(refresh_token)
                        access_token = token_data.get("access_token")
                        headers["Authorization"] = f"Bearer {access_token}"  
                        continue  

                mutation_issue_grow_action = """
                mutation issueGrowAction {
                    issueGrowAction
                }
                """
                result, error = execute_graphql_query(session, url, headers, mutation_issue_grow_action)

                if error:
                    if 'errors' in error and 'UNAUTHORIZED' in error['errors'][0]['message']:
                        logging.info("Access token expired, refreshing token...")
                        token_data = refresh_access_token(refresh_token)
                        access_token = token_data.get("access_token")
                        headers["Authorization"] = f"Bearer {access_token}"  
                        continue 

                mutation_commit_grow_action = """
                mutation commitGrowAction {
                    commitGrowAction
                }
                """
                result, error = execute_graphql_query(session, url, headers, mutation_commit_grow_action)

                if error:
                    if 'errors' in error and 'UNAUTHORIZED' in error['errors'][0]['message']:
                        logging.info("Access token expired, refreshing token...")
                        token_data = refresh_access_token(refresh_token)
                        access_token = token_data.get("access_token")
                        headers["Authorization"] = f"Bearer {access_token}"  
                        continue  

                query_current_user = """
                query CurrentUser {
                    currentUser {
                        name
                        totalPoint
                    }
                }
                """
                response_current_user, error = execute_graphql_query(session, url, headers, query_current_user)

                if error:
                    if 'errors' in error and 'UNAUTHORIZED' in error['errors'][0]['message']:
                        logging.info("Access token expired, refreshing token...")
                        token_data = refresh_access_token(refresh_token)
                        access_token = token_data.get("access_token")
                        headers["Authorization"] = f"Bearer {access_token}"  
                        continue 

                if response_current_user:
                    user_name = response_current_user['data']['currentUser']['name']
                    initial_total_point = response_current_user['data']['currentUser']['totalPoint']

                    mutation_spin = """
                    mutation commitSpinAction {
                        commitSpinAction
                    }
                    """
                    response_spin, error = execute_graphql_query(session, url, headers, mutation_spin)

                    if error:
                        if 'errors' in error and 'UNAUTHORIZED' in error['errors'][0]['message']:
                            logging.info("Access token expired, refreshing token...")
                            token_data = refresh_access_token(refresh_token)
                            access_token = token_data.get("access_token")
                            headers["Authorization"] = f"Bearer {access_token}"  
                            continue  

                    response_current_user_latest, error = execute_graphql_query(session, url, headers, query_current_user)

                    if response_current_user_latest:
                        latest_total_point = response_current_user_latest['data']['currentUser']['totalPoint']
                        print(f"{i + 1}/{num_iterations} | Name: {user_name} | Total Points: {latest_total_point}")

                # Optional: Delay between operations
                time.sleep(1)  # Optional: 1 second delay between operations

            # After completing the iterations
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{current_time} - Waiting for 1 hour before the next batch...")

            # Wait for 1 hour (3600 seconds)
            time.sleep(3600)

        except Exception as e:
            logging.error(f"Error encountered: {e}")
            print_error(f"Error encountered: {e}")

if __name__ == "__main__":
    print_intro()
    main()
