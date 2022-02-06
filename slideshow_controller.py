import logging
import os
from pathlib import Path

class SlideshowController:
    """Controller to handle the slideshow"""

    def __init__(self, sonos_settings):
        self.show_slideshow = getattr(sonos_settings, "show_slideshow", False)
        if self.show_slideshow:
            try:
                images_path = getattr(sonos_settings, "images_path", None)
                self.images_path = Path(images_path)
            except Exception as error:
                self.show_slideshow = False
                _LOGGER.error("Cannot access path: %s, check that it exists", images_path)
                _LOGGER.error(error)
            self.images_files = list(self.images_path.glob("*.png"))
            if len(images_files) is 0:
                self.show_slideshow = False
                _LOGGER.error("There are no png files in path: %s, slideshow not started", images_path)
            self.next_image_index = 0

    def get_next_image(self):
        if self.is_enabled():
            next_image = self.images_files[self.next_image_index]
            self.next_image_index = (self.next_image_index + 1) % self.images_files.size
            return next_image
        else:
            _LOGGER.error("Not getting next image slideshow is disabled!")

    def is_enabled(self):
        return self.show_slideshow

