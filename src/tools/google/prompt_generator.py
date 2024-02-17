def name_prompt(url: str) -> str:
    """
    Generates a query string for a site-specific search.

    This function creates a query string for use with a search engine to find content specifically within the given website.

    Parameters:
    url (str): The URL of the website to search within. This should not include protocol (http/https) or any subdirectories.

    Returns:
    str: A query string formatted for a site-specific search.

    Example:
    >>> name_prompt("example.com")
    'site:example.com'
    """
    return f"site:{url}"


def company_check_prompt(title: str) -> str:
    """
    Generates a query string for searching company profiles on LinkedIn.

    This function forms a query string specifically designed to find company profiles on LinkedIn that match a given title.

    Parameters:
    title (str): The title or keyword to search for in LinkedIn company profiles.

    Returns:
    str: A query string formatted for searching company profiles on LinkedIn.

    Example:
    >>> company_check_prompt("Software")
    'site:linkedin.com intitle:"Software" inurl:company'
    """
    return f'site:linkedin.com intitle:"{title}" inurl:company'


def people_search_prompt(title: str) -> str:
    """
    Generates a query string for searching individual LinkedIn profiles.

    This function creates a query string to find LinkedIn profiles that match a given title. It excludes posts to focus on profile pages.

    Parameters:
    title (str): The title or keyword to search for in individual LinkedIn profiles.

    Returns:
    str: A query string formatted for searching individual profiles on LinkedIn, excluding posts.

    Example:
    >>> people_search_prompt("Engineer")
    'site:linkedin.com intitle:"Engineer" inurl:/in -inurl:/post -inurl:/posts'
    """
    return f'site:linkedin.com intitle:"{title}" inurl:/in -inurl:/post -inurl:/posts -inurl:/jobs'
