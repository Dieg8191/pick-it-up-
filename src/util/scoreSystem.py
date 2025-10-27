class ScoreSystem:
    def __init__(self, total_bushes=100, total_trash=60, max_time=300):
        self.total_bushes = total_bushes
        self.total_trash = total_trash
        self.max_time = max_time

    def calculate_score(self, bushes_destroyed, trash_left, time_remaining):
        # Limitar los valores a rangos válidos
        bushes_destroyed = min(max(bushes_destroyed, 0), self.total_bushes)
        trash_left = min(max(trash_left, 0), self.total_trash)
        time_remaining = max(time_remaining, 0)

        # --- Factores de puntuación ---
        bush_score = (self.total_bushes - bushes_destroyed) * 10     # conservar arbustos
        trash_score = (self.total_trash - trash_left) * 50            # recoger basura
        time_bonus = int(time_remaining * 5)                          # tiempo sobrante

        # --- Puntuación final ---
        score = bush_score + trash_score + time_bonus

        return int(score)
