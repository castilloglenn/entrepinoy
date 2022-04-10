from pygame.sprite import Group


class SpriteGroup(Group):
    """
    Source: https://stackoverflow.com/questions/55233448/pygame-overlapping-sprites-draw-order-based-on-location
    
    Explanation: 
        Problem with rendering when summoning a random crowd with a correct rendering 
        based on y-coordinates
    """
    def by_y(self, spr):
        return spr.rect.y

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sorted(sprites, key=self.by_y):
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []
        