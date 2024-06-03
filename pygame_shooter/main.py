import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter Game")

# Fonts
font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)

# Load images
player_image = pygame.image.load('assets\images\player.png')
enemy_image = pygame.image.load('assets/images/enemy.png')
fast_enemy_image = pygame.image.load('assets/images/fast_enemy.png')
shooting_enemy_image = pygame.image.load('assets/images/shooting_enemy.png')
bullet_image = pygame.image.load('assets/images/bullet.png')
enemy_bullet_image = pygame.image.load('assets/images/enemy_bullet.png')
powerup_image = pygame.image.load('assets/images/powerup.png')

# Load sounds
pygame.mixer.init()
powerup_sound = pygame.mixer.Sound('assets/sounds/powerup.wav')

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5
        self.shield = False
        self.shield_timer = 0
        self.lives = 3  # プレイヤーのライフ

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if self.shield and pygame.time.get_ticks() > self.shield_timer:
            self.shield = False

    def activate_shield(self):
        self.shield = True
        self.shield_timer = pygame.time.get_ticks() + 5000  # シールドは5秒間持続

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bullet, self).__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3)
        self.points = 10  # 各敵が倒された時に加算されるポイント

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# FastEnemy class
class FastEnemy(Enemy):
    def __init__(self):
        super(FastEnemy, self).__init__()
        self.image = fast_enemy_image
        self.speed = random.randint(4, 6)
        self.points = 20  # 各敵が倒された時に加算されるポイント

# ShootingEnemy class
class ShootingEnemy(Enemy):
    def __init__(self):
        super(ShootingEnemy, self).__init__()
        self.image = shooting_enemy_image
        self.shoot_timer = pygame.time.get_ticks()
        self.shoot_interval = 2000  # 2秒ごとに弾を発射
        self.points = 30  # 各敵が倒された時に加算されるポイント

    def update(self):
        super(ShootingEnemy, self).update()
        if pygame.time.get_ticks() - self.shoot_timer > self.shoot_interval:
            self.shoot()
            self.shoot_timer = pygame.time.get_ticks()

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        enemy_bullet_group.add(bullet)

# EnemyBullet class
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(EnemyBullet, self).__init__()
        self.image = enemy_bullet_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# PowerUp class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(PowerUp, self).__init__()
        self.image = powerup_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.type = random.choice(['shield', 'double_shot', 'speed_up'])

    def update(self):
        self.rect.y += 3
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Initialize groups
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
powerup_group = pygame.sprite.Group()

# Score
score = 0

# ゲーム開始時間
start_ticks = pygame.time.get_ticks()

def reset_game():
    global player, player_group, bullet_group, enemy_group, enemy_bullet_group, powerup_group, score, start_ticks
    player = Player()
    player_group = pygame.sprite.Group()
    player_group.add(player)

    bullet_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    enemy_bullet_group = pygame.sprite.Group()
    powerup_group = pygame.sprite.Group()

    score = 0
    start_ticks = pygame.time.get_ticks()

# Main game loop
running = True
game_over = False
clock = pygame.time.Clock()
while running:
    # 経過時間の計算
    elapsed_ticks = pygame.time.get_ticks() - start_ticks
    elapsed_seconds = elapsed_ticks / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    reset_game()
            else:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullet_group.add(bullet)

    if not game_over:
        # Update game state
        keys = pygame.key.get_pressed()
        player.update(keys)
        bullet_group.update()
        enemy_group.update()
        enemy_bullet_group.update()
        powerup_group.update()

        # Check for collisions
        player_powerup_hits = pygame.sprite.spritecollide(player, powerup_group, True)
        for powerup in player_powerup_hits:
            powerup_sound.play()  # パワーアップ効果音の再生
            if powerup.type == 'shield':
                player.activate_shield()
            elif powerup.type == 'double_shot':
                # ダブルショットの処理
                pass
            elif powerup.type == 'speed_up':
                # スピードアップの処理
                pass

        hits = pygame.sprite.groupcollide(enemy_group, bullet_group, True, True)
        for hit in hits:
            score += hit.points

        # プレイヤーが敵または敵の弾に当たった場合
        if pygame.sprite.spritecollide(player, enemy_group, True) or pygame.sprite.spritecollide(player, enemy_bullet_group, True):
            player.lives -= 1
            if player.lives <= 0:
                game_over = True  # ゲームオーバー

        # 時間経過に応じて敵の出現頻度と速度を増加
        spawn_rate = max(0.02, 0.1 - elapsed_seconds / 1000)
        if random.random() < spawn_rate:
            enemy_type = random.choice(['regular', 'fast', 'shooting'])
            if enemy_type == 'regular':
                enemy = Enemy()
            elif enemy_type == 'fast':
                enemy = FastEnemy()
            elif enemy_type == 'shooting':
                enemy = ShootingEnemy()
            enemy_group.add(enemy)

    # Render game objects
    screen.fill((0, 0, 0))
    player_group.draw(screen)
    bullet_group.draw(screen)
    enemy_group.draw(screen)
    enemy_bullet_group.draw(screen)
    powerup_group.draw(screen)

    # Render score
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # Render lives
    lives_text = font.render(f'Lives: {player.lives}', True, WHITE)
    screen.blit(lives_text, (10, 50))

    if game_over:
        game_over_text = font.render('Game Over! Press Space to Restart', True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
