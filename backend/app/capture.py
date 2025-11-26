import asyncio
import logging
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP, ICMP
import json
from datetime import datetime
from .ml.detector import MLDetector
from .rules.detector import RuleDetector

class PacketCapture:
    def __init__(self, mongodb):
        self.mongodb = mongodb
        self.is_capturing = False
        self.packet_count = 0
        self.ml_detector = MLDetector()
        self.rule_detector = RuleDetector()
        self.stats = {
            'total_packets': 0,
            'tcp_packets': 0,
            'udp_packets': 0,
            'icmp_packets': 0,
            'alerts': 0
        }
        
    async def start_capture(self):
        """Démarrer la capture réseau"""
        interface = os.getenv('NETWORK_INTERFACE', 'eth0')
        self.is_capturing = True
        
        def packet_handler(packet):
            asyncio.create_task(self.process_packet(packet))
        
        try:
            logger.info(f"Démarrage de la capture sur l'interface {interface}")
            sniff(iface=interface, prn=packet_handler, store=False)
        except Exception as e:
            logger.error(f"Erreur capture: {e}")
    
    def stop_capture(self):
        """Arrêter la capture"""
        self.is_capturing = False
    
    async def process_packet(self, packet):
        """Traiter chaque paquet capturé"""
        try:
            self.packet_count += 1
            self.stats['total_packets'] += 1
            
            # Extraction des features basiques
            flow_data = self.extract_flow_features(packet)
            if flow_data:
                # Sauvegarder le flow
                await self.mongodb.insert_flow(flow_data)
                
                # Détection par règles
                rule_alerts = self.rule_detector.detect(packet, flow_data)
                for alert in rule_alerts:
                    await self.handle_alert(alert)
                
                # Détection ML
                if self.ml_detector.is_ready():
                    ml_alert = self.ml_detector.detect(flow_data)
                    if ml_alert:
                        await self.handle_alert(ml_alert)
                        
        except Exception as e:
            logger.error(f"Erreur traitement paquet: {e}")
    
    def extract_flow_features(self, packet):
        """Extraire les features du paquet pour ML et analyse"""
        if not packet.haslayer(IP):
            return None
            
        ip_layer = packet[IP]
        flow_data = {
            'timestamp': datetime.now().isoformat(),
            'src_ip': ip_layer.src,
            'dst_ip': ip_layer.dst,
            'protocol': ip_layer.proto,
            'length': len(packet),
            'ttl': ip_layer.ttl
        }
        
        # Features TCP
        if packet.haslayer(TCP):
            tcp_layer = packet[TCP]
            flow_data.update({
                'src_port': tcp_layer.sport,
                'dst_port': tcp_layer.dport,
                'flags': str(tcp_layer.flags),
                'window_size': tcp_layer.window
            })
            self.stats['tcp_packets'] += 1
            
        # Features UDP
        elif packet.haslayer(UDP):
            udp_layer = packet[UDP]
            flow_data.update({
                'src_port': udp_layer.sport,
                'dst_port': udp_layer.dport
            })
            self.stats['udp_packets'] += 1
            
        # Features ICMP
        elif packet.haslayer(ICMP):
            self.stats['icmp_packets'] += 1
            
        return flow_data
    
    async def handle_alert(self, alert_data):
        """Gérer une alerte détectée"""
        self.stats['alerts'] += 1
        alert_data['timestamp'] = datetime.now().isoformat()
        alert_data['id'] = f"alert_{self.stats['alerts']}_{datetime.now().timestamp()}"
        
        # Sauvegarder en base
        await self.mongodb.insert_alert(alert_data)
        
        # Notifier via WebSocket
        # (implémenté plus tard)