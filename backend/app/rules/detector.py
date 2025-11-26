from collections import defaultdict
import time
from datetime import datetime

class RuleDetector:
    def __init__(self):
        self.syn_flood_threshold = 100  # SYN/s
        self.port_scan_threshold = 50   # ports différents/min
        self.land_attack_count = 0
        
        # Structures pour détection d'attaques
        self.syn_count = defaultdict(int)
        self.port_scan_count = defaultdict(lambda: defaultdict(set))
        self.last_reset = time.time()
    
    def detect(self, packet, flow_data):
        alerts = []
        
        # Détection Land Attack
        if self._detect_land_attack(packet):
            alerts.append(self._create_alert(
                "Land Attack", 
                "HIGH", 
                flow_data['src_ip'],
                "Source et destination IP identiques"
            ))
        
        # Détection SYN Flood
        syn_flood = self._detect_syn_flood(packet, flow_data)
        if syn_flood:
            alerts.append(syn_flood)
        
        # Détection Port Scan
        port_scan = self._detect_port_scan(packet, flow_data)
        if port_scan:
            alerts.append(port_scan)
            
        return alerts
    
    def _detect_land_attack(self, packet):
        """Détecter Land Attack (src_ip == dst_ip)"""
        if packet.haslayer(IP):
            ip = packet[IP]
            if ip.src == ip.dst:
                self.land_attack_count += 1
                return True
        return False
    
    def _detect_syn_flood(self, packet, flow_data):
        """Détection SYN Flood"""
        if packet.haslayer(TCP) and packet[TCP].flags == 'S':
            src_ip = flow_data['src_ip']
            current_time = time.time()
            
            # Réinitialiser le compteur toutes les secondes
            if current_time - self.last_reset >= 1:
                self.syn_count.clear()
                self.last_reset = current_time
            
            self.syn_count[src_ip] += 1
            
            if self.syn_count[src_ip] > self.syn_flood_threshold:
                return self._create_alert(
                    "SYN Flood", 
                    "HIGH", 
                    src_ip,
                    f"SYN flood détecté: {self.syn_count[src_ip]} SYN/s"
                )
        return None
    
    def _detect_port_scan(self, packet, flow_data):
        """Détection de scan de ports"""
        if packet.haslayer(TCP):
            src_ip = flow_data['src_ip']
            dst_port = flow_data.get('dst_port')
            
            if dst_port:
                current_minute = int(time.time() / 60)
                self.port_scan_count[src_ip][current_minute].add(dst_port)
                
                # Vérifier si le seuil est dépassé
                if len(self.port_scan_count[src_ip][current_minute]) > self.port_scan_threshold:
                    return self._create_alert(
                        "Port Scan", 
                        "MEDIUM", 
                        src_ip,
                        f"Scan de ports détecté: {len(self.port_scan_count[src_ip][current_minute])} ports différents"
                    )
        return None
    
    def _create_alert(self, alert_type, severity, src_ip, description):
        return {
            'type': alert_type,
            'severity': severity,
            'src_ip': src_ip,
            'description': description,
            'timestamp': datetime.now().isoformat()
        }