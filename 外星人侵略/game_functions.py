import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键。"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """响应关键版本."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


# def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
#                  bullets):
#     """响应按键和鼠标事件。"""
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#         elif event.type == pygame.KEYDOWN:
#             check_keydown_events(event, ai_settings, screen, ship, bullets)
#         elif event.type == pygame.KEYUP:
#             check_keyup_events(event, ship)
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             mouse_x, mouse_y = pygame.mouse.get_pos()
#             check_play_button(ai_settings, screen, stats, sb, play_button,
#                               ship, aliens, bullets, mouse_x, mouse_y)
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
        bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    """当玩家点击Play时开始新游戏。"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #重置游戏设置。
        ai_settings.initialize_dynamic_settings()

        # 隐藏鼠标光标
        pygame.mouse.set_visible(False)

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置记分板图像        
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人和子弹列表。
        aliens.empty()
        bullets.empty()

        #创建一个新舰队并将船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


# def fire_bullet(ai_settings, screen, ship, bullets):
#     """如果还没有达到极限，发射一颗子弹。"""
    #创建新项目符号，添加到项目符号组。
    # if len(bullets) < ai_settings.bullets_allowed:
    #     new_bullet = Bullet(ai_settings, screen, ship)
    #     bullets.add(new_bullet)
def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button):
    """更新屏幕上的图像，并切换到新屏幕."""
    #重新绘制屏幕，每个屏幕都通过循环。
    screen.fill(ai_settings.bg_color)

   #重画所有的子弹，在飞船和外星人后面。
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    #绘制分数信息。
    sb.show_score()

    #如果游戏处于非活动状态，则绘制“播放”按钮。
    if not stats.game_active:
        play_button.draw_button()

   #使最近绘制的屏幕可见。
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新项目符号的位置，并清除旧项目符号."""
    #更新项目符号位置。
    bullets.update()

    #把消失的子弹扔掉。
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets)


def check_high_score(stats, sb):
    """看看有没有新的高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets):
    """对子弹外星碰撞作出反应"""
    #移除所有碰撞过的子弹和外星人。
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        #如果整个舰队被摧毁，开始新的一级。
        bullets.empty()
        ai_settings.increase_speed()

        #提高水平。
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def check_fleet_edges(ai_settings, aliens):
    """如果外星人到达了边缘，请做出适当的反应。"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """放下整个舰队，改变舰队的方向。"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """对被外星人击中的船只作出反应。"""
    if stats.ships_left > 0:
       #减量船离开。
        stats.ships_left -= 1

        # 更新计分板
        sb.prep_ships()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    #清空外星人和子弹列表。
    aliens.empty()
    bullets.empty()

    #创建一个新舰队，并使船居中。
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # 暂停
    sleep(0.5)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
                        bullets):
    """检查是否有外星人到达屏幕底部。"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 把它当作船撞了一样对待。
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    检查舰队是否处于边缘，
然后更新舰队中所有外星人的位置。
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 外星人船碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # 寻找屏幕底部的外星人。
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def get_number_aliens_x(ai_settings, alien_width):
    """确定适合一行的外星人数量."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """确定适合屏幕的外星人行数."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人，并将其放在行中."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建一个完整的外星人舰队."""
    # create的外星人，外星人和找到号码在一行。
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

   #创建外星人舰队。
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)
