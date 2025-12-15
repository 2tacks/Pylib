import json  
import os  
from datetime import datetime  
from typing import Optional, Dict, List  
from plyer import notification  
import requests  
from concurrent.futures import ThreadPoolExecutor  
import logging  

class UsernameModule:  
    """Advanced username reconnaissance module - top 100 social platforms"""  
    
    def __init__(self):  
        self.target_username: Optional[str] = None  
        self.output_folder: Optional[str] = None  
        self.results = {}  
        self.logger = self._setup_logger()  
        self._setup_platforms()  
    
    def _setup_logger(self) -> logging.Logger:  
        """Configure advanced logging system"""  
        logger = logging.getLogger("UsernameModule")  
        logger.setLevel(logging.DEBUG)  
        handler = logging.FileHandler("username_module.log")  
        formatter = logging.Formatter(  
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'  
        )  
        handler.setFormatter(formatter)  
        logger.addHandler(handler)  
        return logger  
    
    def _setup_platforms(self):  
        """Initialize top 100 social media platforms"""  
        self.platforms = {  
            # Social Networks  
            'facebook': 'https://www.facebook.com/{0}',  
            'twitter': 'https://www.twitter.com/{0}',  
            'instagram': 'https://www.instagram.com/{0}',  
            'tiktok': 'https://www.tiktok.com/@{0}',  
            'snapchat': 'https://www.snapchat.com/add/{0}',  
            'pinterest': 'https://www.pinterest.com/{0}',  
            'linkedin': 'https://www.linkedin.com/in/{0}',  
            'reddit': 'https://www.reddit.com/user/{0}',  
            'youtube': 'https://www.youtube.com/@{0}',  
            'twitch': 'https://www.twitch.tv/{0}',  
            
            # Messaging & Communication  
            'telegram': 'https://t.me/{0}',  
            'discord': 'https://discord.com/users/{0}',  
            'whatsapp': 'https://wa.me/{0}',  
            'viber': 'https://viber.click/{0}',  
            'signal': 'https://signal.me/#p/{0}',  
            
            # Photo & Video  
            'flickr': 'https://www.flickr.com/photos/{0}',  
            'vimeo': 'https://www.vimeo.com/{0}',  
            'dailymotion': 'https://www.dailymotion.com/{0}',  
            'rumble': 'https://rumble.com/{0}',  
            'odysee': 'https://odysee.com/@{0}',  
            
            # Blogging & Content  
            'medium': 'https://medium.com/@{0}',  
            'hashnode': 'https://hashnode.com/@{0}',  
            'wordpress': 'https://{0}.wordpress.com',  
            'substack': 'https://substack.com/@{0}',  
            'patreon': 'https://www.patreon.com/{0}',  
            
            # Gaming  
            'steam': 'https://steamcommunity.com/search/users/{0}',  
            'xbox': 'https://www.xbox.com/en-US/xbox-live/friends/search/{0}',  
            'psn': 'https://www.playstation.com/en-us/psn/{0}',  
            'epicgames': 'https://www.epicgames.com/site/en-US/home/{0}',  
            'fortnite': 'https://fortnite.gg/en/profile/{0}',  
            
            # Developer & Tech  
            'github': 'https://www.github.com/{0}',  
            'gitlab': 'https://www.gitlab.com/{0}',  
            'bitbucket': 'https://www.bitbucket.org/{0}',  
            'stackoverflow': 'https://stackoverflow.com/users/{0}',  
            'devto': 'https://dev.to/{0}',  
            
            # Dating & Social  
            'tinder': 'https://tinder.com/@{0}',  
            'bumble': 'https://bumble.com/{0}',  
            'okcupid': 'https://www.okcupid.com/profile/{0}',  
            'hinge': 'https://hinge.co/{0}',  
            'meetup': 'https://www.meetup.com/{0}',  
            
            # Shopping & Marketplace  
            'ebay': 'https://www.ebay.com/usr/{0}',  
            'amazon': 'https://www.amazon.com/s?k={0}',  
            'etsy': 'https://www.etsy.com/shop/{0}',  
            'mercari': 'https://www.mercari.com/u/{0}',  
            'depop': 'https://www.depop.com/{0}',  
            
            # Finance & Crypto  
            'coinbase': 'https://www.coinbase.com/{0}',  
            'kraken': 'https://www.kraken.com/{0}',  
            'binance': 'https://www.binance.com/{0}',  
            'opensea': 'https://opensea.io/{0}',  
            'raydium': 'https://raydium.io/fusion/{0}',  
            
            # Fitness & Health  
            'strava': 'https://www.strava.com/athletes/{0}',  
            'myfitnesspal': 'https://www.myfitnesspal.com/profile/{0}',  
            'fitbit': 'https://www.fitbit.com/user/{0}',  
            'peloton': 'https://www.peloton.com/profile/{0}',  
            
            # Music & Podcasts  
            'spotify': 'https://open.spotify.com/user/{0}',  
            'soundcloud': 'https://soundcloud.com/{0}',  
            'bandcamp': 'https://{0}.bandcamp.com',  
            'anchor': 'https://anchor.fm/{0}',  
            'apple_music': 'https://music.apple.com/profile/{0}',  
            
            # Travel & Lifestyle  
            'airbnb': 'https://www.airbnb.com/users/show/{0}',  
            'booking': 'https://www.booking.com/profile.en.html?{0}',  
            'tripadvisor': 'https://www.tripadvisor.com/members/{0}',  
            'foursquare': 'https://foursquare.com/{0}',  
            
            # Job & Networking  
            'indeed': 'https://www.indeed.com/profile/{0}',  
            'glassdoor': 'https://www.glassdoor.com/Profile/profile.htm?{0}',  
            'angellist': 'https://angel.co/{0}',  
            'producthunt': 'https://www.producthunt.com/@{0}',  
            
            # Community & Forums  
            'quora': 'https://www.quora.com/profile/{0}',  
            'nextdoor': 'https://nextdoor.com/member/{0}',  
            'ycombinator': 'https://news.ycombinator.com/user?id={0}',  
            'dribbble': 'https://dribbble.com/{0}',  
            'behance': 'https://www.behance.net/{0}',  
            
            # Additional Platforms  
            'aol': 'https://aim.aol.com/{0}',  
            'icq': 'https://www.icq.com/{0}',  
            'skype': 'https://web.skype.com/{0}',  
            'line': 'https://line.me/R/ti/p/{0}',  
            'wechat': 'https://weixin.qq.com/{0}',  
            
            # Regional Networks  
            'vk': 'https://vk.com/{0}',  
            'ok': 'https://ok.ru/{0}',  
            'viber': 'https://viber.click/{0}',  
            'weibo': 'https://www.weibo.com/u/{0}',  
            'qq': 'https://qq.com/{0}',  
        }  
        self.logger.info(f"Initialized {len(self.platforms)} social media platforms")  
    
    def search(self, username: str) -> 'UsernameModule':  
        """  
        Search username across social platforms  
        
        Args:  
            username: Username to search  
            
        Returns:  
            self: For method chaining  
        """  
        self.target_username = username  
        self.logger.info(f"Target username set: {username}")  
        return self  
    
    def output(self, folder_path: str) -> 'UsernameModule':  
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
    
    def execute(self) -> 'UsernameModule':  
        """  
        Execute username search across all platforms  
        
        Returns:  
            self: For method chaining  
        """  
        if not self.target_username:  
            self.logger.error("No target username specified")  
            return self  
        
        if not self.output_folder:  
            self.output_folder = "./username_results"  
            os.makedirs(self.output_folder, exist_ok=True)  
        
        self.logger.info(f"Starting username reconnaissance on: {self.target_username}")  
        
        with ThreadPoolExecutor(max_workers=20) as executor:  
            futures = {  
                executor.submit(self._check_platform, platform, url): platform  
                for platform, url in self.platforms.items()  
            }  
            
            for future in futures:  
                try:  
                    result = future.result(timeout=10)  
                    if result:  
                        self.results.update(result)  
                except Exception as e:  
                    self.logger.error(f"Platform check error: {e}")  
        
        self._save_results()  
        self.logger.info(f"Username reconnaissance completed. Found {len(self.results)} matches")  
        return self  
    
    def notify(self) -> 'UsernameModule':  
        """  
        Send desktop notification  
        
        Returns:  
            self: For method chaining  
        """  
        notification.notify(  
            title="Username Module Complete",  
            message="Done! Data Sent.",  
            app_name="Advanced OSINT Tool",  
            timeout=10  
        )  
        self.logger.info("Notification sent")  
        return self  
    
    def _check_platform(self, platform: str, url_template: str) -> Optional[Dict]:  
        """Check if username exists on platform"""  
        try:  
            formatted_url = url_template.format(self.target_username)  
            headers = {  
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'  
            }  
            
            response = requests.head(formatted_url, headers=headers, timeout=5, allow_redirects=True)  
            
            # Different platforms return different status codes for existing users  
            if response.status_code in [200, 301, 302, 303]:  
                self.logger.info(f"Found on {platform}: {formatted_url}")  
                return {platform: formatted_url}  
            
        except requests.exceptions.Timeout:  
            self.logger.debug(f"Timeout on {platform}")  
        except requests.exceptions.ConnectionError:  
            self.logger.debug(f"Connection error on {platform}")  
        except Exception as e:  
            self.logger.debug(f"Error checking {platform}: {e}")  
        
        return None  
    
    def _save_results(self):  
        """Save results to JSON log file"""  
        if not self.results:  
            self.logger.warning("No results to save")  
            return  
        
        log_file = os.path.join(  
            self.output_folder,  
            f"Log{len(os.listdir(self.output_folder)) + 1}.json"  
        )  
        
        try:  
            with open(log_file, 'w') as f:  
                json.dump(self.results, f, indent=2)  
            self.logger.info(f"Results saved to {log_file}")  
        except Exception as e:  
            self.logger.error(f"Failed to save results: {e}")