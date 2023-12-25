import pygame

def draw_text_with_border(
    screen: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    inside_color: pygame.Color,
    border_color: pygame.Color,
    border_size: float,
    positon: pygame.math.Vector2,
):
    # new_text = text
    # for i in emoji_list:
    #     for _ in range(text.count(f"<{i}>")):
    #         smile_msg_pos = text.find(f"<{i}>")
    #         new_text = text.replace(f"<{i}>", "  ")
    #
    #         no_smile_one = font.render(text.split(f"<{i}>")[0], True, inside_color)
    #
    #         smile_pos = positon.x + no_smile_one.get_width()
    #
    #         if smile_msg_pos != -1:
    #             screen.blit(imgs.emojis[f"{i}"], [smile_pos, positon.y])

    inside = font.render(text, True, inside_color)
    border = font.render(text, True, border_color)

    screen.blit(border, pygame.math.Vector2(positon.x - border_size, positon.y))
    screen.blit(border, pygame.math.Vector2(positon.x + border_size, positon.y))
    screen.blit(border, pygame.math.Vector2(positon.x, positon.y - border_size))
    screen.blit(border, pygame.math.Vector2(positon.x, positon.y + border_size))
    screen.blit(inside, positon)

    return inside