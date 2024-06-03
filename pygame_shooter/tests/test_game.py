import unittest
import pygame
from main import Player, PowerUp, FastEnemy, ShootingEnemy

class TestGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))

    def test_player_initialization(self):
        player = Player()
        self.assertEqual(player.rect.center, (400, 550))

    def test_bullet_initialization(self):
        bullet = Bullet(400, 500)
        self.assertEqual(bullet.rect.center, (400, 500))

    def test_enemy_initialization(self):
        enemy = Enemy()
        self.assertTrue(0 <= enemy.rect.x <= 800 - enemy.rect.width)
        self.assertTrue(-100 <= enemy.rect.y <= -40)

    def test_powerup_initialization(self):
        powerup = PowerUp(400, 300)
        self.assertIn(powerup.type, ['shield', 'double_shot', 'speed_up'])
        self.assertEqual(powerup.rect.center, (400, 300))

    def test_player_shield_activation(self):
        player = Player()
        player.activate_shield()
        self.assertTrue(player.shield)
        self.assertGreater(player.shield_timer, pygame.time.get_ticks())

    def test_player_collects_shield_powerup(self):
        player = Player()
        powerup = PowerUp(400, 300)
        powerup.type = 'shield'
        powerup.rect.center = player.rect.center
        player_group = pygame.sprite.Group()
        player_group.add(player)
        powerup_group = pygame.sprite.Group()
        powerup_group.add(powerup)

        collision = pygame.sprite.spritecollide(player, powerup_group, True)
        for item in collision:
            if item.type == 'shield':
                player.activate_shield()

        self.assertTrue(player.shield)

    def test_fast_enemy_movement(self):
        fast_enemy = FastEnemy()
        initial_y = fast_enemy.rect.y
        fast_enemy.update()
        self.assertGreater(fast_enemy.rect.y, initial_y)

    def test_shooting_enemy_shooting(self):
        shooting_enemy = ShootingEnemy()
        initial_bullet_count = len(enemy_bullet_group)
        shooting_enemy.shoot()
        self.assertEqual(len(enemy_bullet_group), initial_bullet_count + 1)

    def tearDown(self):
        pygame.quit()

if __name__ == '__main__':
    unittest.main()
