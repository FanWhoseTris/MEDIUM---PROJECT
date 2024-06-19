from sklearn.cluster import KMeans
import numpy
import matplotlib.pyplot as mpl
import pygame

show_matplotlib_window = False
def show_matplotlib():
    global show_matplotlib_window
    show_matplotlib_window = True

pygame.init()

screen = pygame.display.set_mode((1200, 700))

pygame.display.set_caption("Xu ly anh")

clock = pygame.time.Clock()

running = True

BACKGROUND = (214, 214, 214)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0, 0)
BACKGROUND_PANEL = (249, 255, 230)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (147, 153, 35)
PURPLE = (255, 0, 255)
SKY = (0, 255, 255)
ORANGE = (255, 125, 25)
GRAPE = (100, 25, 125)
GRASS = (55, 155, 65)

cluster = 0

# create text
font = pygame.font.SysFont('sans', 40)
fonttext = pygame.font.SysFont('sans', 30)
font_small = pygame.font.SysFont('sans', 10)

textlink = font.render('PATH', True, BLACK)
textimg = font.render('IMAGE', True, BLACK)
text_plus = font.render('+', True, BLACK)
text_minus = font.render('-', True, BLACK)
text_color = font.render('COLOR=', True, BLACK)
text_change = font.render('CHANGE', True, BLACK)
text_save = font.render('SAVE', True, BLACK)
path = ''
while running:
    clock.tick(60)

    screen.fill(SKY)

    # Draw
    pygame.draw.rect(screen, BLACK, (45, 30, 1105, 70))
    pygame.draw.rect(screen, WHITE, (162, 32, 986, 66))
    pygame.draw.rect(screen, RED, (45, 30, 115, 70))
    screen.blit(textlink, (55, 25))
    screen.blit(textimg, (55, 60))
    text_path = fonttext.render(path, True, BLACK)
    screen.blit(text_path, (160, 45))
    pygame.draw.rect(screen, WHITE, (80, 190, 80, 80))
    screen.blit(text_plus, (110, 205))
    pygame.draw.rect(screen, WHITE, (250, 190, 80, 80))
    screen.blit(text_minus, (280, 205))
    screen.blit(text_color, (510, 215))
    pygame.draw.rect(screen, WHITE, (170, 435, 245, 70))
    screen.blit(text_change, (222, 452))
    pygame.draw.rect(screen, WHITE, (800, 435, 245, 70))
    screen.blit(text_save, (860, 452))
    text_color = font.render('COLOR=' + str(cluster), True, BLACK)

    # create mouse position
    mx, my = pygame.mouse.get_pos()
    if 0 <= mx <= 1200 and 0 <= my <= 700:
        text_mouse = font_small.render("(" + str(mx) + "," + str(my) + ")", True, BLACK)
        screen.blit(text_mouse, (mx + 10, my))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(
                "-----------------------------------------------------------------------------------------------------------------------------------------------------")
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 80 <= mx <= 160 and 190 <= my <= 270:
                cluster += 1
                print("press K+ ="+str(cluster))
            elif 250 <= mx <= 330 and 190 <= my <= 270:
                if cluster >= 0: cluster-=1
                print("press K- ="+str(cluster))
            elif 170 <= mx <= 415 and 435 <= my <= 505:
                try:
                    img = mpl.imread(path + '.jpg')
                    w = img.shape[0]
                    h = img.shape[1]
                    img = img.reshape(h * w, 3)
                    print(img.shape)
                    kmean = KMeans(n_clusters=cluster).fit(img)
                    print("1")
                    labels = kmean.predict(img)
                    print("2")
                    clusters = kmean.cluster_centers_
                    print("3")
                    img2 = numpy.zeros((w, h, 3), dtype=numpy.uint8)
                    print("4")
                    index = 0
                    print("5")
                    for i in range(w):
                        for j in range(h):
                            label_of_pixel = labels[index]
                            img2[i][j] = clusters[label_of_pixel]
                            index += 1
                    print("change")
                except:
                    print("error path")
            elif 800 <= mx <= 1045 and 435 <= my <= 505:
                try:
                    show_matplotlib()
                    print("pressed save")
                except:
                    print("error")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("Input:", path)  # In ra giá trị đã nhập
                path = ""  # Xóa giá trị đã nhập sau khi xử lý

            elif event.key == pygame.K_BACKSPACE:
                path = path[:-1]  # Xóa ký tự cuối cùng
            else:
                path += event.unicode  # Thêm ký tự đã nhấn vào input
    if show_matplotlib_window:
        # Hiển thị hình ảnh trong cửa sổ matplotlib
        mpl.imshow(img2)
        mpl.show()

        # Đặt lại biến show_matplotlib_window để ngăn việc hiển thị liên tục
        show_matplotlib_window = False
    pygame.display.flip()

pygame.quit()



