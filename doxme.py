import time
import random
import os
from datetime import datetime, timedelta

os.system('title DoxMe')

proxy_ports = [443, 80, 1080, 1194, 22, 53, 8291, 3128, 8080]

proxy_errors = [
   ("408", "Request Timeout"),
   ("504", "Gateway Timeout"),
   ("403", "Forbidden"),
   ("404", "Not Found"),
   ("502", "Bad Gateway"),
   ("522", "Connection Timed Out"),
   ("530", "Login Authentication Failed"),
   ("ERR_NET_RESET", "Connection Reset"),
   ("ERR_PROXY_CONN", "Proxy Connection Failed"),
   ("ERR_TUNNEL_CONN", "Tunnel Establishment Failed"),
   ("ERR_DNS_FAIL", "DNS Resolution Failed"),
   ("ERR_TIMEOUT", "Connection Timed Out"),
]

def color_latency(latency_ms):
   min_latency = 150
   max_latency = 600
   ratio = (latency_ms - min_latency) / (max_latency - min_latency)
   ratio = max(0.0, min(1.0, ratio))

   r = int(255 * ratio)
   g = int(255 * (1 - ratio))
   b = 0

   return f"\033[38;2;{r};{g};{b}m~   {latency_ms}ms\033[0m"

def censor_ip(ip):
   parts = ip.split('.')
   censored = []
   for i, part in enumerate(parts):
      if i < 1:
         censored.append(part) 
      else:
         censored.append(part[:-1] + '*') if len(part) > 1 else censored.append('*')
   return '.'.join(censored)

def timestamp():
   return datetime.now().strftime("[%H:%M:%S]")

def rgb_fade(text, block_size=10):
   result = ""
   for i, char in enumerate(text):
      pos = i % block_size
      middle = (block_size - 1) / 2
      ratio = 1 - abs(pos - middle) / middle  # normalized 0 to 1 to 0
      min_gb = 30
      max_gb = 255
      g = 255
      b = int(min_gb + (max_gb - min_gb) * ratio)
      r = int(min_gb + (max_gb - min_gb) * ratio)
      result += f"\033[38;2;{r};{g};{b}m{char}"
   return result + "\033[0m"

def rgb_fade2(text, block_size=10):
   result = ""
   for i, char in enumerate(text):
      pos = i % block_size
      middle = (block_size - 1) / 2
      ratio = 1 - abs(pos - middle) / middle
      min_gb = 30
      max_gb = 255
      g = int(min_gb + (max_gb - min_gb) * ratio)
      b = int(min_gb + (max_gb - min_gb) * ratio)
      r = 255
      result += f"\033[38;2;{r};{g};{b}m{char}"
   return result + "\033[0m"

def generate_history(entries=34, interval_minutes=10):
   now = datetime.now()
   #print(rgb_fade(f"[{now.strftime('%H:%M:%S')}] Booting from session memory...\n"))
   
   for i in range(entries):
      jitter_seconds = random.randint(-2, 2)
      fake_time = now - timedelta(minutes=(entries - i) * interval_minutes) + timedelta(seconds=jitter_seconds)
      time_str = fake_time.strftime("[%H:%M:%S]")
      ip = ".".join(str(random.randint(10, 255)) for _ in range(5))
      censored_ip = censor_ip(ip).center(23)
      port = str(random.choice(proxy_ports)).center(6)
      latency = random.randint(150, 600)
      latency_colored = color_latency(latency)
      if random.random() < 0.05:
         error_code, error_msg = random.choice(proxy_errors)
         error_code_str = error_code.center(7)
         error_msg_str = error_msg.center(28)
         print(rgb_fade2(
            f"{time_str} [proxies.txt] [!] Error: {censored_ip} ({error_code_str}|{error_msg_str})"
         ))
      else:
         line_start = f"{time_str} [proxies.txt] [/] Rotated IP: {censored_ip} (Ping   "
         line_end = f") [{port}]"
         print(rgb_fade(line_start) + latency_colored + rgb_fade(line_end))

def rotate_ip():
   ip = ".".join(str(random.randint(10, 255)) for _ in range(5))
   censored_ip = censor_ip(ip)
   port = random.choice(proxy_ports)
   latency = random.randint(150, 600)

   time_str = timestamp()
   ip_str = censored_ip.center(23)
   port_str = str(port).center(6)

   if random.random() < 0.05:
      error_code, error_msg = random.choice(proxy_errors)
      error_code_str = error_code.center(7)
      error_msg_str = error_msg.center(28)
      print(rgb_fade2(
         f"{time_str} [proxies.txt] [!] Error: {ip_str} ({error_code_str}|{error_msg_str})"
      ))
      return "no"
   else:
      line_start = f"{time_str} [proxies.txt] [/] Rotated IP: {ip_str} (Ping   "
      line_end = f") [{port_str}]"
      latency_colored = color_latency(latency)
      print(rgb_fade(line_start) + latency_colored + rgb_fade(line_end))
      return "ok"


def run():
   os.system('cls')
   print(rgb_fade(f"{timestamp()} Secure Proxy Chain Initialized from [proxies.txt]"))
   print(rgb_fade(f"{timestamp()} Monitoring traffic, rotating endpoints...\n"))
   
   generate_history()

   while True:
      if rotate_ip() == "ok":
         time.sleep(600) # you can change the rotation interval here
         
if __name__ == "__main__":
   run()
