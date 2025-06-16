
from requests import get, RequestException

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate", 
}

def scan_request(url:str, headers:dict = HEADERS, cookies:dict = None) -> dict:
    """
    Makes a GET request to specified URL and returns all response data.
    :param url: URL to make GET request to.
    :param headers: Headers to include in GET request.
    :param cookies: Cookies to include in GET request.
    :return: Dictionary containing response data including status code, content, and URL.
    :rtype: dict
    """

    try:
        # Attempt to make GET request to specified URL with provided headers and cookies
        data = get(url, headers=headers, cookies=cookies)

    except RequestException as e:
        # Return error and 500 status in event of a request failure
        return {
            "status_code": 500,
            "content": str(e),
            "url": url
        }
    
    # Return response data including status code, content, and URL
    return {
        "status_code": data.status_code,
        "content": data.text,
        "url": data.url
    }
    
def scan_validate_response(site_data:dict, validation_method:str, validation_key:str | int) -> str:
    """
    Validates the response page is in fact a user page and not a generic error page or redirect the is providing a 200 response.
    Some pages may return various response codes that can indicate a valid user hit even if the content is not acessable.
    :param site_data: Site data taken from initial GET request.
    :param validation_method: How the site should be validated (e.g., "RegEx", "Status", "URL").
    :param validation_key: Key to validate against the response data based on the validation method.
    :return: Validation status of the response data.
        - "Valid": The site has been validated and is a user page.
        - "Invalid": The site is garunteed to not be a user page.
        - "Unknown": The site cannot be confiremed to be a user page or not.
    :rtype: str
    """

    match validation_method:
        case "RegEx":
            # TODO: Implement RegEx Validation
            return "Unknown"  # Placeholder for RegEx validation
        case "Status":
            return "Valid" if site_data['status_code'] == validation_key else "Invalid"
        case "URL":
            return "Valid" if validation_key in site_data['url'] else "Invalid"
        case _:
            # TODO: Implement plugin support for custom validation methods
            return "Unknown"


def scan_site_verify(site:dict, uname:str) -> list:
    """
    Scans the provided site to harvest any necessary information and verifies the site response.
    :param site: Site data from manifest containing all necessary information to scan the site.
    :param uname: Username to scan for on the site.
    :return: Array containing all scan results in the format: [sitename, url, response_code, validation_status, validation_method, hit_status]
    :rtype: list
    """

    # TODO: Add support for custom fields implemented by plugins && Implement plugin function call point to process response data

    # Initialize result array with site name, URL, and validation method
    result = [site['name'], site['url'].format(uname), None, None, site['validation_method'], None]

    # Attempt to retrieve the site data
    site_data = scan_request(site['url'].format(uname))

    # Assign initial response values to the result array
    result[2] = site_data['status_code']
    result[5] = "Hit" if site_data['status_code'] == 200 and site_data['content'] != "" else "Miss"

    # If the site data is a 500 response code, most likely there was a malformed request or the site is down
    # In such an event we will not waste time validating the response
    # Otherwise, validate the response based on the validation method and key
    if site_data['status_code'] != 500:
        result[3] = scan_validate_response(site_data, site['validation_method'], site['validation_key'])
    else:
        result[3] = "Unknown"

    return result