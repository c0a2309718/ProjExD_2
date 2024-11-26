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
    """
    go_bg = pg.Surface((WIDTH, HEIGHT))  # 画面全体を覆うSurfaceを作成 
    pg.draw.rect(go_bg, (0, 0, 0), (0, 0, WIDTH, HEIGHT)) 
    go_bg.set_alpha(200)  # 半透明度を設定
    screen.blit(go_bg, [0, 0])  
    # フォントを設定し、「Game Over」のテキストを作成
    font = pg.font.Font(None, 80) 
    text = font.render("Game Over", True, (255, 255, 255)) 
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # 画面中央にテキストを配置
    # 泣いているこうかとんの画像を読み込む
    cry_kk_img = pg.image.load("fig/8.png")  
    cry_kk_img = pg.transform.rotozoom(cry_kk_img, 0, 1)  
    # 左側のこうかとん画像の位置を設定
    cry_kk_rct_left = cry_kk_img.get_rect()  
    cry_kk_rct_left.center = WIDTH / 2 - 180, HEIGHT / 2 - 10  # 左のこうかとんをテキストの左側に配置
    # 右側のこうかとん画像の位置を設定
    cry_kk_rct_right = cry_kk_img.get_rect()  
    cry_kk_rct_right.center = WIDTH / 2 + 180, HEIGHT / 2 - 10  # 右のこうかとんをテキストの右側に配置
    # テキストと画像を画面に描画
    screen.blit(text, text_rect)  
    screen.blit(cry_kk_img, cry_kk_rct_left)  
    screen.blit(cry_kk_img, cry_kk_rct_right) 
    # 画面を更新して描画内容を表示
    pg.display.update()
    # 5秒間停止して表示を維持
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    サイズの異なる爆弾Surfaceを要素としたリストと加速度リストを生成して返す
    戻り値:
        - bb_imgs: サイズが異なる爆弾Surfaceのリスト
        - bb_accs: 爆弾の加速度リスト（1から10）
    """
    bb_imgs = []  # 爆弾Surfaceのリスト
    bb_accs = [a for a in range(1, 11)]  # 加速度リスト（1～10）

    for r in range(1, 11):  # 爆弾のサイズを10段階で用意
        bb_img = pg.Surface((20 * r, 20 * r))  # サイズに応じたSurfaceを生成
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r) # 半径に応じた円を描画
        bb_img.set_colorkey((0, 0, 0)) #外枠をなくす
        bb_imgs.append(bb_img) # リストに追加

    return bb_imgs, bb_accs 


def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    """
    飛ぶ方向に従ってこうかとん画像を切り替える
    引数：移動量の合計値タプルsum_mv
    戻り値：sum_mvルに対応する向きの画像Surfaceを返す
    """


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_imgs, bb_accs = init_bb_imgs()  # 爆弾Surfaceリストと加速度リストを初期化
    bb_rct = bb_imgs[0].get_rect()  # 初期爆弾サイズのRectを取得
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0  
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            game_over(screen) # ゲームオーバー処理を呼び出す
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
        # 爆弾のサイズと加速度を段階的に変化させる
        avx = vx*bb_accs[min(tmr//500, 9)]# 加速度を適用した横方向速度
        avy = vy*bb_accs[min(tmr//500, 9)]# 加速度を適用した縦方向速度
        bb_img = bb_imgs[min(tmr//500, 9)]# 現在の段階の爆弾Surface
        # 爆弾のRectを更新（中心を維持）
        bb_center = bb_rct.center  # 現在の中心座標を取得
        bb_rct = bb_img.get_rect() # 新しい爆弾Surfaceに基づいてRectを取得
        bb_rct.center = bb_center  

        bb_rct.move_ip(avx, avy)
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
