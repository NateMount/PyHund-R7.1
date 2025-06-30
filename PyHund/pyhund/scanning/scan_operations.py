
from requests import get, RequestException
from re import match

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate", 
    "Pragma": "no-cache",
    "Referer": "https://www.google.com/",
    "upgrade-insecure-requests": "1"
}

def scan_request(url:str, headers:dict = HEADERS, cookies:dict = None) -> dict:
    """
    Scan Request
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
        # Return response data including status code, content, and URL
        return {
            "status_code": data.status_code,
            "content": data.text,
            "url": data.url
        }

    except RequestException as e:
        # Return error and 500 status in event of a request failure
        return {
            "status_code": 500,
            "content": str(e),
            "url": url
        }
    

def scan_validate_response(site_data:dict, validation_method:str, validation_key:str | int) -> str:
    """
    Scanning Validate Response
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

    match validation_method.lower():
        case "regex":
            pattern:str = validation_key.lstrip('~')

            if match(pattern, site_data['content']) != None:
                return 'Invalid' if validation_key.startswith('~') else "Valid"
            
            return "Valid" if validation_key.startswith('~') else "Invalid"
        case "status":
            return "Valid" if site_data['status_code'] == validation_key else "Invalid"
        case "url":
            return ("Valid" if validation_key[1:] not in site_data['url'] else "Invalid") if validation_key.startswith('~') else ("Valid" if validation_key in site_data['url'] else "Invalid")
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

    # Attempt to retrieve the site data
    site_data:dict = scan_request(site['url'].format(uname), headers=site.get('headers', HEADERS), cookies=site.get('cookies', None))

    return [
        site['name'],
        site['url'].format(uname),
        site_data['status_code'],
        "Unknown" if site_data["status_code"] == 500 else scan_validate_response(site_data, site['validation_method'], site['validation_key']),
        site['validation_method'],
        "Hit" if site_data['status_code'] == 200 and site_data['content'] != "" else "Miss"
    ]