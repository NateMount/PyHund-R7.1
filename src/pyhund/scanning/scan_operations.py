
from requests import get, RequestException

HEADERS = {

}

def scan_request(url:str) -> dict:
    """
    Makes a GET request to specified URL and returns all response data.
    :param url: URL to make GET request to.
    """

    data = get(url, headers=HEADERS, cookies=None)
    
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
            pass # TODO: Implement RegEx Validation
        case "Status":
            return "Valid" if site_data['status_code'] == validation_key else "Invalid"
        case "URL":
            return "Valid" if validation_key in site_data['url'] else "Invalid"
        case _:
            return "Unknown"

def scan_site_verify(site:dict, uname:str) -> list:
    """
    Scans the provided site to harvest any necessary information and verifies the site response.
    :param site: Site data from manifest containing all necessary information to scan the site.
    :param uname: Username to scan for on the site.
    :return: Array containing all scan results in the format: [sitename, url, response_code, validation_status, validation_method, hit_status]
    :rtype: list
    """

    # Initialize result array with site name, URL, and validation method
    result = [site['name'], site['url'].format(uname), None, None, site['validation_method'], None]

    # Attempt to retrieve the site data
    site_data = scan_request(site['url'].format(uname))

    # Assign initial response values to the result array
    result[2] = site_data['status_code']
    result[5] = "Hit" if site_data['status_code'] == 200 and site_data['content'] != "" else "Miss"

    result[3] = scan_validate_response(site_data, site['validation_method'], site['validation_key'])

    return result