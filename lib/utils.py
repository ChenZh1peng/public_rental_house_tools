"""common utility functions
"""
def join_url(url1, url2):
    """合并url的两部分，主要处理两部分中间的 /

    Args:
        url1 (str): url前半部分，如"https://a.b.com"
        url2 (str): url后半部分，如"/api/user/get"
    """
    url1_suffix_slash = url1[-1] == '/'
    url2_prefix_slash = url2[0] == '/'
    if  (not url1_suffix_slash and url2_prefix_slash) or \
        (url1_suffix_slash and not url2_prefix_slash):
        return url1 + url2
    if not url1_suffix_slash and not url2_prefix_slash:
        return url1 + '/' + url2
    if url1_suffix_slash and url2_prefix_slash:
        return url1.rstrip('/') + url2
