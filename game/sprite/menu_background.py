from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame import image as pyimage
from pygame import draw, transform


class MenuBackground(Sprite):
    """
    This handles the size and position of a menu background.
    """
    def __init__(self, screen: Surface, 
                 screen_ratio: float,
                 image: pyimage = None,
                 color: tuple[int] = None):
        super().__init__()
        
        self.enable = True
        self.screen = screen
        
        self.x = int(self.screen.get_rect().width * ((1 -screen_ratio) / 2))
        self.y = int(self.screen.get_rect().height * ((1 -screen_ratio) / 2))
        self.width = int(self.screen.get_rect().width * screen_ratio)
        self.height = int(self.screen.get_rect().height * screen_ratio)
        
        self.image = Surface((self.width,self.height))
        
        if image != None:
            self.image = transform.scale(image, (self.width, self.height)).convert_alpha()
            
        self.rect = self.image.get_rect()
        
        if color != None:
            self.gradient_increment = 16
            self.gradient_lighten = True
            self.starting_color = color
            self.ending_color = tuple(map(lambda x: self.color_amplify(x), self.starting_color))
            self.fill_gradient()
        
        self.rect.topleft = (self.x, self.y)
        
        
    def fill_gradient(self, vertical=True, forward=True):
        """
        (Modified) Source: http://www.pygame.org/wiki/GradientCode
        Explanation: Needed a gradient effect on the menu overlay
        """
        x1,x2 = self.rect.left, self.rect.right
        y1,y2 = self.rect.top, self.rect.bottom
        if vertical: 
            h = y2-y1
        else:        
            h = x2-x1
            
        if forward: 
            a, b = self.starting_color, self.ending_color
        else:       
            b, a = self.starting_color, self.ending_color
        rate = (
            float(b[0]-a[0])/h,
            float(b[1]-a[1])/h,
            float(b[2]-a[2])/h
        )
        fn_line = draw.line
        if vertical:
            for line in range(y1,y2):
                color = (
                    min(max(a[0]+(rate[0]*(line-y1)),0),255),
                    min(max(a[1]+(rate[1]*(line-y1)),0),255),
                    min(max(a[2]+(rate[2]*(line-y1)),0),255)
                )
                fn_line(self.image, color, (x1,line), (x2,line))
        else:
            for col in range(x1,x2):
                color = (
                    min(max(a[0]+(rate[0]*(col-x1)),0),255),
                    min(max(a[1]+(rate[1]*(col-x1)),0),255),
                    min(max(a[2]+(rate[2]*(col-x1)),0),255)
                )
                fn_line(self.image, color, (col,y1), (col,y2))
                
                
    def color_amplify(self, x):
        if self.gradient_lighten:
            return min(255, x + self.gradient_increment)
        return max(0, x - self.gradient_increment)
        
    
    def update(self):
        if not self.enable:
            self.close()
        
        self.screen.blit(self.image, self.rect)
        
        
    def check_clicked(self, click_coordinates):
        if not self.rect.collidepoint(click_coordinates):
            self.close()
            
    
    def close(self):
        self.enable = False
        
