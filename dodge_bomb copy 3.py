import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    bb_img  = pg.Surface((20, 20))
    pg.draw.circle(bb_img , (255, 0, 0), (10, 10), 10)
    bb_img .set_colorkey((0, 0, 0))

    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    bb_rct = bb_img.get_rect()
    bb_rct.center = x, y

    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    vx = 0
    vy = 0
    DELTA = {pg.K_UP:(0, -5), 
             pg.K_DOWN:(0, 5),
             pg.K_LEFT:(-5, 0),
             pg.K_RIGHT:(5, 0)}
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        screen.blit(bb_img, bb_rct)
        bb_rct.move_ip(vx, vy)
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, delta in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += delta[0]
                sum_mv[1] += delta[1]
        kk_rct.move_ip(sum_mv)
        screen.blit(kk_img, kk_rct)
        pg.display.update()
        tmr += 1
        vx += 5
        vy += 5
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
