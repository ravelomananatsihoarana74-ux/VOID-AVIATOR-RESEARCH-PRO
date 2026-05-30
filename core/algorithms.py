import random
import math

class AviatorEngine:
    """
    Simulateur de logique Aviator basé sur le concept Provably Fair.
    """
    def __init__(self):
        self.house_edge = 0.03  # 3% d'avantage maison standard

    def calculate_crash(self, server_seed, client_seed, nonce):
        """
        Algorithme simplifié inspiré du Provably Fair.
        Utilise un hash pour déterminer le point de crash.
        """
        # En réalité, c'est un HMAC-SHA512
        import hashlib
        combined = f"{server_seed}:{client_seed}:{nonce}".encode()
        h = hashlib.sha256(combined).hexdigest()
        
        # Conversion du hash en nombre
        int_val = int(h[:8], 16)
        
        # Formule type : (2^32 / (val + 1)) * (1 - edge)
        # Mais ici on simplifie pour la simulation
        if int_val % 33 == 0:  # Instant crash 1.00x
            return 1.00
            
        return round(max(1.0, (100 / (100 - (int_val % 99 + 1))) * (1 - self.house_edge)), 2)

class StrategyManager:
    """
    Bibliothèque de stratégies mathématiques.
    """
    @staticmethod
    def martingale(history, last_bet, won):
        return last_bet * 2 if not won else 1.0

    @staticmethod
    def fibonacci(history, index):
        # Suite de Fibonacci pour les paliers
        a, b = 1, 1
        for _ in range(index):
            a, b = b, a + b
        return a

    @staticmethod
    def dalembert(current_bet, won):
        if won:
            return max(1.0, current_bet - 1)
        return current_bet + 1

    @staticmethod
    def signal_analyzer(history):
        """
        Analyse les tendances (Pattern Recognition).
        """
        if len(history) < 3: return "WAIT"
        
        # Exemple : 3 crashs bas (< 2x) -> Probabilité forte d'un pic > 2x
        low_streak = all(x < 2.0 for x in history[-3:])
        if low_streak:
            return "HIGH_PROBABILITY_NEXT"
        return "STABLE"
