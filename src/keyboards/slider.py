from . import buttons

class Slider:

    data = []
    left_index = 0
    right_index = 9
    
    @classmethod
    def get_current_page(cls):
        data = cls.data[cls.left_index:cls.right_index] 
        return buttons.MarkUp.ratingResultsMarkUp(data) 
    
    @classmethod
    def go_right(cls):
        cls.left_index = cls.right_index + 1
        cls.right_index += 10
        
        if cls.right_index <= len(cls.data):
            return cls.get_current_page()
        
        return None
    
    @classmethod
    def go_left(cls):
        cls.right_index = cls.left_index
        cls.left_index -= 10
        
        if cls.left_index >= 0:
            return cls.get_current_page()
        
        return None