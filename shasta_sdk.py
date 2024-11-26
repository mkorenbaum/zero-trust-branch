import requests
import time

# Constants (replace with actual token and base URL as needed)
BASE_URL = "https://api-stg.shastacloud.com"
MSP_ORG_ID = "317"
BEARER_TOKEN = "your_bearer_token_here"
MAX_RETRIES = 5  # Maximum number of retries
RETRY_BACKOFF_FACTOR = 2  # Exponential backoff factor (in seconds)

# Headers for authentication
HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "application/json"
}

def handle_request_with_retries(method, url, headers=None, params=None, json=None):
    """
    Handles API requests with retry mechanism for 429 errors.

    Parameters:
        method (str): HTTP method (e.g., "GET", "POST", "DELETE").
        url (str): URL of the API endpoint.
        headers (dict): Headers to include in the request.
        params (dict, optional): Query parameters for the request.
        json (dict, optional): JSON body for the request.

    Returns:
        Response object: The HTTP response.

    Raises:
        Exception: If retries exceed MAX_RETRIES.
    """
    retries = 0
    while retries <= MAX_RETRIES:
        response = requests.request(method, url, headers=headers, params=params, json=json)
        if response.status_code == 429:  # Too Many Requests
            wait_time = RETRY_BACKOFF_FACTOR ** retries
            print(f"Rate limited. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
            retries += 1
        else:
            response.raise_for_status()  # Raise an error for non-200 status codes
            return response
    raise Exception(f"Failed after {MAX_RETRIES} retries due to rate limiting.")

def get_business_orgs(offset=0, limit=10, order="DESC", order_by="orgId"):
    """
    Retrieves a list of business organizations.

    Parameters:
        offset (int): Pagination offset.
        limit (int): Number of results to retrieve per request.
        order (str): Sort order ("ASC" or "DESC").
        order_by (str): Field to sort by.

    Returns:
        dict: JSON response containing business organizations.
    """
    url = f"{BASE_URL}/organization/{MSP_ORG_ID}/child"
    params = {"offset": offset, "limit": limit, "order": order, "orderBy": order_by}
    response = handle_request_with_retries("GET", url, headers=HEADERS, params=params)
    return response.json()

def create_business_org(org_display_name, org_type_id, parent_org_id, address):
    """
    Creates a new business organization.

    Parameters:
        org_display_name (str): Display name of the organization.
        org_type_id (int): Type ID of the organization.
        parent_org_id (int): Parent organization ID.
        address (str): Address of the organization.

    Returns:
        dict: JSON response containing the created organization's details.
    """
    url = f"{BASE_URL}/organization"
    payload = {
        "orgDisplayName": org_display_name,
        "orgTypeId": org_type_id,
        "parentOrgId": parent_org_id,
        "phone": "",
        "notes": "",
        "billingRecipients": "",
        "orgAddress": {"addressLine": address},
        "billingAddress": {"addressLine": address}
    }
    response = handle_request_with_retries("POST", url, headers=HEADERS, json=payload)
    return response.json()

def find_business_org(search_query, offset=0, limit=10, order="DESC", order_by="orgId"):
    """
    Searches for a specific business organization.

    Parameters:
        search_query (str): Name or other identifier of the organization to search for.
        offset (int): Pagination offset.
        limit (int): Number of results to retrieve per request.
        order (str): Sort order ("ASC" or "DESC").
        order_by (str): Field to sort by.

    Returns:
        dict: JSON response containing the search results.
    """
    url = f"{BASE_URL}/organization/{MSP_ORG_ID}/child"
    params = {"search": search_query, "offset": offset, "limit": limit, "order": order, "orderBy": order_by}
    response = handle_request_with_retries("GET", url, headers=HEADERS, params=params)
    return response.json()

def remove_business_org(org_id):
    """
    Removes a business organization.

    Parameters:
        org_id (int): ID of the organization to remove.

    Returns:
        int: HTTP status code of the response.
    """
    url = f"{BASE_URL}/organization/{org_id}"
    response = handle_request_with_retries("DELETE", url, headers=HEADERS)
    return response.status_code

def get_venues(org_id, offset=0, limit=10, order="DESC", order_by="venueId", search_query=None):
    """
    Retrieves venues for a specific organization.

    Parameters:
        org_id (int): ID of the organization.
        offset (int): Pagination offset.
        limit (int): Number of results to retrieve per request.
        order (str): Sort order ("ASC" or "DESC").
        order_by (str): Field to sort by.
        search_query (str, optional): Name or other identifier of the venue to search for.

    Returns:
        dict: JSON response containing the venues.
    """
    url = f"{BASE_URL}/venues"
    params = {"orgId": org_id, "offset": offset, "limit": limit, "order": order, "orderBy": order_by}
    if search_query:
        params["search"] = search_query
    response = handle_request_with_retries("GET", url, headers=HEADERS, params=params)
    return response.json()

def create_venue(org_id, venue_name, address):
    """
    Creates a new venue for an organization.

    Parameters:
        org_id (int): ID of the organization.
        venue_name (str): Name of the venue.
        address (str): Address of the venue.

    Returns:
        dict: JSON response containing the created venue's details.
    """
    url = f"{BASE_URL}/venues"
    payload = {
        "orgId": org_id,
        "parentVenueId": 0,
        "venueName": venue_name,
        "state": 1,
        "venueType": 1,
        "venueAddress": {"addressLine": address},
        "shippingAddress": {"addressLine": address}
    }
    response = handle_request_with_retries("POST", url, headers=HEADERS, json=payload)
    return response.json()

def remove_venue(venue_id):
    """
    Removes a venue.

    Parameters:
        venue_id (int): ID of the venue to remove.

    Returns:
        int: HTTP status code of the response.
    """
    url = f"{BASE_URL}/venues/{venue_id}"
    response = handle_request_with_retries("DELETE", url, headers=HEADERS)
    return response.status_code

def get_infrastructure_by_org(org_id):
    """
    Retrieves infrastructure for a specific organization.

    Parameters:
        org_id (int): ID of the organization.

    Returns:
        dict: JSON response containing the infrastructure details.
    """
    url = f"{BASE_URL}/infrastructure/organization/{org_id}"
    response = handle_request_with_retries("GET", url, headers=HEADERS)
    return response.json()

def get_infrastructure_by_venue(venue_id):
    """
    Retrieves infrastructure for a specific venue.

    Parameters:
        venue_id (int): ID of the venue.

    Returns:
        dict: JSON response containing the infrastructure details.
    """
    url = f"{BASE_URL}/infrastructure/venue/{venue_id}"
    response = handle_request_with_retries("GET", url, headers=HEADERS)
    return response.json()

def get_infra_types():
    """
    Retrieves infrastructure types available for the organization.

    Returns:
        dict: JSON response containing the infrastructure types.
    """
    url = f"{BASE_URL}/infrastructure/infratype"
    params = {"orgId": MSP_ORG_ID}
    response = handle_request_with_retries("GET", url, headers=HEADERS, params=params)
    return response.json()

def add_infrastructure(org_id, venue_id, infra_type_id, mac_address, infra_display_name):
    """
    Adds new infrastructure for a venue.

    Parameters:
        org_id (int): ID of the organization.
        venue_id (int): ID of the venue.
        infra_type_id (int): Type ID of the infrastructure.
        mac_address (str): MAC address of the infrastructure.
        infra_display_name (str): Display name of the infrastructure.

    Returns:
        dict: JSON response containing the created infrastructure details.
    """
    url = f"{BASE_URL}/infrastructure"
    payload = {
        "venueId": venue_id,
        "orgId": org_id,
        "infraTypeId": infra_type_id,
        "macAddress": mac_address,
        "serialNumber": "",
        "assetTag": "",
        "infraDisplayName": infra_display_name,
        "sourceId": 1,
        "realInfra": False
    }
    response = handle_request_with_retries("POST", url, headers=HEADERS, json=payload)
    return response.json()

def remove_infrastructure(infra_id):
    """
    Removes an infrastructure item.

    Parameters:
        infra_id (int): ID of the infrastructure to remove.

    Returns:
        int: HTTP status code of the response.
    """
    url = f"{BASE_URL}/infrastructure/{infra_id}"
    response = handle_request_with_retries("DELETE", url, headers=HEADERS)
    return response.status_code

# Example usage of the functions
if __name__ == "__main__":
    try:
        # Example: Get business orgs
        orgs = get_business_orgs()
        print("Business Orgs:", orgs)
        
        # Add more logic as needed
    except Exception as e:
        print(f"An error occurred: {e}")