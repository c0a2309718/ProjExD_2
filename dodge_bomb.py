import os
import random
import sys
import time

import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP: (0, -5), 
             pg.K_DOWN: (0, 5),
             pg.K_LEFT: (-5, 0),
             pg.K_RIGHT: (5, 0),
    }
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外か判定
    引数：こうかとんRect or 爆弾Rect
    戻り値：真理値タプル（横，縦）/画面内：True、画面外：False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate
    
def game_over(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に画面を暗くし、メッセージと画像を表示する
    引数：ゲームオーバーscreen
    戻り値：なし
    """
    go_bg = pg.Surface((WIDTH, HEIGHT))  # 画面全体を覆うSurfaceを作成 
    pg.draw.rect(go_bg, (0, 0, 0), (0, 0, WIDTH, HEIGHT))  # Surfaceを黒で塗りつぶす
    go_bg.set_alpha(200)  # 半透明度を設定（200: ほぼ不透明）
    screen.blit(go_bg, [0, 0])  # 半透明の黒い背景を画面に描画
    # フォントを設定し、「Game Over」のテキストを作成
    font = pg.font.Font(None, 80)  # フォントサイズ80でフォントオブジェクトを作成
    text = font.render("Game Over", True, (255, 255, 255))  # 白い文字で「Game Over」を描画
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # 画面中央にテキストを配置
    # 泣いているこうかとんの画像を読み込む
    cry_kk_img = pg.image.load("fig/8.png")  # 泣いているこうかとんの画像を読み込み
    cry_kk_img = pg.transform.rotozoom(cry_kk_img, 0, 1)  # 画像サイズを調整（拡大率1倍）
    # 左側のこうかとん画像の位置を設定
    cry_kk_rct_left = cry_kk_img.get_rect()  # 画像のRectを取得
    cry_kk_rct_left.center = WIDTH / 2 - 180, HEIGHT / 2 - 10  # 左のこうかとんをテキストの左側に配置
    # 右側のこうかとん画像の位置を設定
    cry_kk_rct_right = cry_kk_img.get_rect()  # 画像のRectを取得
    cry_kk_rct_right.center = WIDTH / 2 + 180, HEIGHT / 2 - 10  # 右のこうかとんをテキストの右側に配置
    # テキストと画像を画面に描画
    screen.blit(text, text_rect)  # 「Game Over」のテキストを描画
    screen.blit(cry_kk_img, cry_kk_rct_left)  # 左のこうかとん画像を描画
    screen.blit(cry_kk_img, cry_kk_rct_right)  # 右のこうかとん画像を描画
    # 画面を更新して描画内容を表示
    pg.display.update()
    # 5秒間停止して表示を維持
    time.sleep(5)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img  = pg.Surface((20, 20)) #爆弾用の空surface
    pg.draw.circle(bb_img , (255, 0, 0), (10, 10), 10) #爆弾円を描く
    bb_img .set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5 #爆弾速度ベクトル
    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            game_over(screen) #ゲームオーバー
            return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        # こうかとんが画面外なら、元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy) #爆弾が動く
        # 爆弾が画面外なら符号を反転
        yoko, tate = check_bound(bb_rct)
        if not yoko: #横にはみ出る
            vx *= -1
        if not tate: #縦にはみ出る
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
