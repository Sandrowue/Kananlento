def render_centered_text_lines(screen, font, text_and_colors, padding_perc=0.05):
    screen_w = screen.get_width()
    screen_h = screen.get_height()
    text_imgs = [
        font.render(text, True, color)
        for (text, color) in text_and_colors
    ]
    padding = int(screen_h * padding_perc)
    total_text_height = sum(img.get_height() for img in text_imgs)
    total_padding = (len(text_imgs) - 1) * padding

    menu_height = total_text_height + total_padding

    y = (screen_h - menu_height) / 2

    for text_img in text_imgs:
        x = (screen_w - text_img.get_width()) / 2
        screen.blit(text_img, (x, y))
        y += padding + text_img.get_height()