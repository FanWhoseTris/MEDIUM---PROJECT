import pygame
import os

class Game:
    WIDTH, HEIGHT = 900, 500
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    FPS = 60
    VEL = 5
    BULLET_VEL = 7
    MAX_BULLETS = 3
    P_WIDTH, P_HEIGHT = 70, 70
    LEFT_HIT = pygame.USEREVENT + 1
    RIGHT_HIT = pygame.USEREVENT + 2
    def __init__(self):
        pygame.font.init()
        pygame.mixer.init()
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Solo???")

        self.BORDER = pygame.Rect(self.WIDTH // 2 - 5, 0, 10, self.HEIGHT)

        self.HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
        self.WINNER_FONT = pygame.font.SysFont('comicsans', 100)

        self.LEFT_IMAGE = pygame.image.load(os.path.join('../assets', 'left.png'))
        self.LEFT = pygame.transform.scale(self.LEFT_IMAGE, (self.P_WIDTH, self.P_HEIGHT))

        self.RIGHT_IMAGE = pygame.image.load(os.path.join('../assets', 'right.png'))
        self.RIGHT = pygame.transform.scale(self.RIGHT_IMAGE, (self.P_WIDTH, self.P_HEIGHT))

        self.SPACE = pygame.transform.scale(pygame.image.load(os.path.join('../assets', 'env.png')), (self.WIDTH, self.HEIGHT))

    def draw(self, right, left, right_bullets, left_bullets, right_health, left_health):
        self.WIN.blit(self.SPACE, (0, 0))

        right_health_text = self.HEALTH_FONT.render(str(right_health) + ":" + "-" * right_health, 1, self.RED)
        left_health_text = self.HEALTH_FONT.render(str(left_health) + ":" + "-" * left_health, 1, self.RED)

        self.WIN.blit(right_health_text,
                      (self.WIDTH - right_health_text.get_width() - 10,
                       self.HEIGHT - right_health_text.get_height() - 10))
        self.WIN.blit(left_health_text, (10, self.HEIGHT - left_health_text.get_height() - 10))

        self.WIN.blit(self.LEFT, (left.x, left.y))
        self.WIN.blit(self.RIGHT, (right.x, right.y))

        for bullet in right_bullets:
            pygame.draw.circle(self.WIN, (0, 0, 255), (bullet.x + bullet.width // 2, bullet.y + bullet.height // 2),
                               7)

        for bullet in left_bullets:
            pygame.draw.circle(self.WIN, (127, 0, 255), (bullet.x + bullet.width // 2, bullet.y + bullet.height // 2),
                               7)

        pygame.display.update()

    def left_move(self, keys_pressed, left):
        if keys_pressed[pygame.K_a] and left.x - self.VEL > 0:
            left.x -= self.VEL
        if keys_pressed[pygame.K_d] and left.x + self.VEL + left.width < self.BORDER.x:
            left.x += self.VEL
        if keys_pressed[pygame.K_w] and left.y - self.VEL > 0:
            left.y -= self.VEL
        if keys_pressed[pygame.K_s] and left.y + self.VEL + left.height < self.HEIGHT - 15:
            left.y += self.VEL

    def right_move(self, keys_pressed, right):
        if keys_pressed[pygame.K_LEFT] and right.x - self.VEL > self.BORDER.x + self.BORDER.width:
            right.x -= self.VEL
        if keys_pressed[pygame.K_RIGHT] and right.x + self.VEL + right.width < self.WIDTH:
            right.x += self.VEL
        if keys_pressed[pygame.K_UP] and right.y - self.VEL > 0:
            right.y -= self.VEL
        if keys_pressed[pygame.K_DOWN] and right.y + self.VEL + right.height < self.HEIGHT - 15:
            right.y += self.VEL

    def bullet_move(self, left_bullets, right_bullets, left, right):
        for bullet in left_bullets:
            bullet.x += self.BULLET_VEL
            if right.colliderect(bullet):
                pygame.event.post(pygame.event.Event(self.RIGHT_HIT))
                left_bullets.remove(bullet)
            elif bullet.x > self.WIDTH:
                left_bullets.remove(bullet)

        for bullet in right_bullets:
            bullet.x -= self.BULLET_VEL
            if left.colliderect(bullet):
                pygame.event.post(pygame.event.Event(self.LEFT_HIT))
                right_bullets.remove(bullet)
            elif bullet.x < 0:
                right_bullets.remove(bullet)

    def draw_winner(self, text):
        draw_text = self.WINNER_FONT.render(text, 1, self.WHITE)
        self.WIN.blit(draw_text, (self.WIDTH / 2 - draw_text.get_width() / 2, self.HEIGHT / 2 - draw_text.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(2000)

    def show_end_menu(self, winner_text):
        end_menu_font = pygame.font.Font("../assets/Arial.ttf", 50)
        winner_font = pygame.font.SysFont('comicsans', 70)

        run = True
        while run:
            self.WIN.fill(self.BLACK)
            winner_title = winner_font.render(winner_text, 1, self.WHITE)
            self.WIN.blit(winner_title, (self.WIDTH / 2 - winner_title.get_width() / 2, 100))

            play_again_text = end_menu_font.render("Nhấn 'R' để Chơi lại Hiệp nữa !", 1, self.WHITE)
            quit_text = end_menu_font.render("Nhấn 'Q' để thoát", 1, self.WHITE)

            self.WIN.blit(play_again_text, (self.WIDTH / 2 - play_again_text.get_width() / 2, self.HEIGHT / 2 - 50))
            self.WIN.blit(quit_text, (self.WIDTH / 2 - quit_text.get_width() / 2, self.HEIGHT / 2 + 50))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return True
                    if event.key == pygame.K_q:
                        return False

    def main_menu(self):
        menu_font = pygame.font.SysFont('comicsans', 100)
        button_font = pygame.font.Font("../assets/Arial.ttf",
                                       50)
        play_button = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT // 2 - 50, 200, 65)
        instructions_button = pygame.Rect(self.WIDTH // 2 - 230, self.HEIGHT // 2 + 50, 480, 65)
        run = True
        while run:
            self.WIN.fill(self.BLACK)
            title_text = menu_font.render("SOLO ???", 1, self.WHITE)
            self.WIN.blit(title_text, (self.WIDTH / 2 - title_text.get_width() / 2, 30))
            pygame.draw.rect(self.WIN, self.WHITE, play_button)
            pygame.draw.rect(self.WIN, self.WHITE, instructions_button)

            play_text = button_font.render("Chơi!", 1, self.BLACK)
            instructions_text = button_font.render("Hướng dẫn sử dụng", 1, self.BLACK)

            self.WIN.blit(play_text,
                          (play_button.x + play_button.width // 2 - play_text.get_width() // 2, play_button.y))
            self.WIN.blit(instructions_text, (
                instructions_button.x + instructions_button.width // 2 - instructions_text.get_width() // 2,
                instructions_button.y))

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if play_button.collidepoint(mouse_pos):
                        return

                    if instructions_button.collidepoint(mouse_pos):
                        self.show_instructions()

    def show_instructions(self):
        instruction_font = pygame.font.Font("../assets/Arial.ttf", 30)
        run = True
        while run:
            self.WIN.fill(self.BLACK)

            instructions = [
                "Hướng dẫn Chơi:",
                "Người chơi Trái: dùng W/A/S/D để di chuyển, nút T để đánh.",
                "Người chơi Phải : dùng các nút di chuyển </>/v/^, nút P để đánh.",
                "Nhấn Q để trở về HOME."
            ]

            for i, line in enumerate(instructions):
                text = instruction_font.render(line, 1, self.WHITE)
                self.WIN.blit(text, (self.WIDTH / 2 - text.get_width() / 2, 100 + i * 40))

            creator_text = instruction_font.render("cre: Trisphan", 1, self.WHITE)
            self.WIN.blit(creator_text, (10, self.HEIGHT - 40))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return

    def main(self):
        self.main_menu()
        right = pygame.Rect(700, 300, self.P_WIDTH, self.P_HEIGHT)
        left = pygame.Rect(100, 300, self.P_WIDTH, self.P_HEIGHT)

        right_bullets = []
        left_bullets = []

        right_health = 10
        left_health = 10

        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t and len(left_bullets) < self.MAX_BULLETS:
                        bullet = pygame.Rect(left.x + left.width, left.y + left.height // 2 - 5, 20, 10)
                        left_bullets.append(bullet)

                    if event.key == pygame.K_p and len(right_bullets) < self.MAX_BULLETS:
                        bullet = pygame.Rect(right.x, right.y + right.height // 2 - 5, 20, 10)
                        right_bullets.append(bullet)

                if event.type == self.RIGHT_HIT:
                    right_health -= 1

                if event.type == self.LEFT_HIT:
                    left_health -= 1

            winner_text = ""
            if right_health <= 0:
                winner_text = "Left Wins!"

            if left_health <= 0:
                winner_text = "Right Wins!"

            if winner_text != "":
                self.draw_winner(winner_text)
                if not self.show_end_menu(winner_text):
                    return
                else:
                    self.main()
                    return

            keys_pressed = pygame.key.get_pressed()
            self.left_move(keys_pressed, left)
            self.right_move(keys_pressed, right)

            self.bullet_move(left_bullets, right_bullets, left, right)

            self.draw(right, left, right_bullets, left_bullets, right_health, left_health)

if __name__ == "__main__":
    game = Game()
    game.main()
