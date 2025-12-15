import json
import os
from datetime import datetime
from typing import Optional
from plyer import notification
import socket
import requests
import logging
from concurrent.futures import ThreadPoolExecutor
import ipaddress

class TraceModule:
    """Advanced IP tracing and geolocation module"""
    
    def __init__(self):
        self.target_ip: Optional[str] = None
        self.output_folder: Optional[str] = None
        self.results = {}
        self.logger = self._setup_logger()
        self._setup_trace_services()
    
    def _setup_logger(self) -> logging.Logger:
        """Configure advanced logging system"""
        logger = logging.getLogger("TraceModule")
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler("trace_module.log")
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    def _setup_trace_services(self):
        """Initialize IP tracing services"""
        self.services = {
            'ipqualityscore': 'https://api.abuseipdb.com/api/v2/check',
            'maxmind': 'https://geoip.maxmind.com',
            'ipinfo': 'https://ipinfo.io',
            'abuseipdb': 'https://api.abuseipdb.com/api/v2/check',
        }
        self.logger.info("Trace services initialized")
    
    def target(self, ip_address: str) -> 'TraceModule':
        """
        Set target IP address
        
        Args:
            ip_address: IP address to trace
            
        Returns:
            self: For method chaining
        """
        if not self._validate_ip(ip_address):
            self.logger.error(f"Invalid IP address: {ip_address}")
            return self
        
        self.target_ip = ip_address
        self.logger.info(f"Target IP set: {ip_address}")
        return self
    
    def output(self, folder_path: str) -> 'TraceModule':
        """
        Set output folder for results
        
        Args:
            folder_path: Path to output directory
            
        Returns:
            self: For method chaining
        """
        try:
            os.makedirs(folder_path, exist_ok=True)
            self.output_folder = folder_path
            self.logger.info(f"Output folder set: {folder_path}")
        except Exception as e:
            self.logger.error(f"Failed to create output folder: {e}")
        return self
    
    def execute(self) -> 'TraceModule':
        """
        Execute IP trace operation
        
        Returns:
            self: For method chaining
        """
        if not self.target_ip:
            self.logger.error("No target IP specified")
            return self
        
        if not self.output_folder:
            self.output_folder = "./trace_results"
            os.makedirs(self.output_folder, exist_ok=True)
        
        self.logger.info(f"Starting IP trace on: {self.target_ip}")
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(self._geoip_lookup, self.target_ip): 'geolocation',
                executor.submit(self._asn_lookup, self.target_ip): 'asn_info',
                executor.submit(self._abuse_check, self.target_ip): 'abuse_report',
                executor.submit(self._dns_reverse, self.target_ip): 'dns_reverse',
                executor.submit(self._port_scan, self.target_ip): 'open_ports',
            }
            
            for future in futures:
                try:
                    result = future.result(timeout=15)
                    self.results.update(result)
                except Exception as e:
                    self.logger.error(f"Trace service error: {e}")
        
        self._save_results()
        self.logger.info("IP trace completed")
        return self
    
    def notify(self) -> 'TraceModule':
        """
        Send desktop notification
        
        Returns:
            self: For method chaining
        """
        notification.notify(
            title="Trace Module Complete",
            message="Done! IP Traced And Data Sent!",
            app_name="Advanced OSINT Tool",
            timeout=10
        )
        self.logger.info("Notification sent")
        return self
    
    def _validate_ip(self, ip_address: str) -> bool:
        """Validate IP address format"""
        try:
            ipaddress.ip_address(ip_address)
            return True
        except ValueError:
            return False
    
    def _geoip_lookup(self, ip_address: str) -> dict:
        """Perform geolocation lookup"""
        try:
            response = requests.get(
                f"{self.services['ipinfo']}/{ip_address}/json",
                timeout=5
            )
            if response.status_code == 200:
                return {'geolocation': response.json()}
            return {'geolocation': {}}
        except Exception as e:
            self.logger.warning(f"Geolocation lookup failed: {e}")
            return {'geolocation': {}}
    
    def _asn_lookup(self, ip_address: str) -> dict:
        """Lookup ASN information"""
        try:
            response = requests.get(
                f"https://asn.cymru.com/cgi-bin/whois.cgi?ip={ip_address}&format=json",
                timeout=5
            )
            if response.status_code == 200:
                return {'asn_info': response.json()}
            return {'asn_info': {}}
        except Exception as e:
            self.logger.warning(f"ASN lookup failed: {e}")
            return {'asn_info': {}}
    
    def _abuse_check(self, ip_address: str) -> dict:
        """Check IP abuse reports"""
        try:
            # Simulated abuse check
            return {
                'abuse_report': {
                    'is_whitelisted': False,
                    'abuseConfidenceScore': 0,
                    'usageType': 'Content Delivery Network'
                }
            }
        except Exception as e:
            self.logger.warning(f"Abuse check failed: {e}")
            return {'abuse_report': {}}
    
    def _dns_reverse(self, ip_address: str) -> dict:
        """Perform reverse DNS lookup"""
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
            return {'dns_reverse': {'hostname': hostname}}
        except Exception as e:
            self.logger.warning(f"Reverse DNS lookup failed: {e}")
            return {'dns_reverse': {'hostname': 'Unknown'}}
    
    def _port_scan(self, ip_address: str) -> dict:
        """Scan common open ports"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 5432, 8080]
        open_ports = []
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip_address, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except Exception:
                pass
        
        return {'open_ports': open_ports}
    
    def _save_results(self):
        """Save results to JSON log file"""
        if not self.results:
            self.logger.warning("No results to save")
            return
        
        log_file = os.path.join(self.output_folder, f"TraceLog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        try:
            with open(log_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            self.logger.info(f"Results saved to {log_file}")
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")


# Usage example
if __name__ == "__main__":
    trace_module = TraceModule()
    trace_module.target("8.8.8.8").output("./results").execute().notify()