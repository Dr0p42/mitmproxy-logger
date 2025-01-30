import json
import time
import os
from urllib.parse import urlparse
import hashlib

class RequestLogger:
    def __init__(self):
        # Create a base directory for logs
        self.base_dir = f"mitm_logs_{int(time.time())}"
        os.makedirs(self.base_dir, exist_ok=True)

    def request(self, flow):
        # Store the timestamp when request starts
        flow.request.timestamp_start = time.time()
        
        timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        parsed_url = urlparse(flow.request.pretty_url)
        domain = parsed_url.netloc
        
        # Create domain directory
        domain_dir = os.path.join(self.base_dir, domain)
        os.makedirs(domain_dir, exist_ok=True)

        # Create unique filename using timestamp and hash of URL
        url_hash = hashlib.md5(flow.request.pretty_url.encode()).hexdigest()[:8]
        filename = f"{timestamp}_{url_hash}.json"
        filepath = os.path.join(domain_dir, filename)

        # Prepare request data
        log_entry = {
            "timestamp": time.time(),
            "method": flow.request.method,
            "url": flow.request.pretty_url,
            "path": parsed_url.path,
            "query": dict(flow.request.query),
            "headers": dict(flow.request.headers),
            "cookies": dict(flow.request.cookies),
            "content": flow.request.content.decode('utf-8', 'ignore') if flow.request.content else None
        }

        # Write to file
        with open(filepath, 'w') as f:
            json.dump(log_entry, f, indent=2)

    def response(self, flow):
        timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        parsed_url = urlparse(flow.request.pretty_url)
        domain = parsed_url.netloc
        
        # Create domain directory
        domain_dir = os.path.join(self.base_dir, domain)
        os.makedirs(domain_dir, exist_ok=True)

        # Create unique filename using timestamp and hash of URL
        url_hash = hashlib.md5(flow.request.pretty_url.encode()).hexdigest()[:8]
        filename = f"{timestamp}_{url_hash}_response.json"
        filepath = os.path.join(domain_dir, filename)

        # Prepare response data
        log_entry = {
            "timestamp": time.time(),
            "method": flow.request.method,
            "url": flow.request.pretty_url,
            "path": parsed_url.path,
            "query": dict(flow.request.query),
            "request_headers": dict(flow.request.headers),
            "request_cookies": dict(flow.request.cookies),
            "request_content": flow.request.content.decode('utf-8', 'ignore') if flow.request.content else None,
            "request_timestamp": getattr(flow.request, 'timestamp_start', None),
            "status_code": flow.response.status_code,
            "reason": flow.response.reason,
            "response_headers": dict(flow.response.headers),
            "response_cookies": dict(flow.response.cookies),
            "response_content": flow.response.content.decode('utf-8', 'ignore') if flow.response.content else None,
            "request_url": flow.request.pretty_url,
            "request_method": flow.request.method
        }

        # Write to file
        with open(filepath, 'w') as f:
            json.dump(log_entry, f, indent=2)

addons = [RequestLogger()]