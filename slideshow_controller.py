import logging
from datetime import datetime
from pathlib import Path

from croniter import croniter

_LOGGER = logging.getLogger(__name__)

class SlideshowController:
    """Controller to handle the slideshow"""

    def __init__(self, sonos_settings):
        self.show_slideshow = getattr(sonos_settings, "show_slideshow", False)
        self.slideshow_timers = getattr(sonos_settings, "slideshow_timers", [])
        if self.show_slideshow:
            try:
                images_path = getattr(sonos_settings, "images_path", None)
                self.images_path = Path(images_path)
            except Exception as error:
                self.show_slideshow = False
                _LOGGER.error("Cannot access path: %s, check that it exists", images_path)
                _LOGGER.error(error)
            self.images_files = list(self.images_path.glob("*.png"))
            if len(self.images_files) is 0:
                self.show_slideshow = False
                _LOGGER.error("There are no png files in path: %s, slideshow not started", images_path)
            self.next_image_index = 0


    def get_next_image(self):
        if self.is_enabled():
            next_image = self.images_files[self.next_image_index]
            self.next_image_index = (self.next_image_index + 1) % len(self.images_files)
            return next_image
        else:
            _LOGGER.error("Not getting next image slideshow is disabled!")

    def is_enabled(self):
        time = datetime.now()
        is_enabled = self.show_slideshow and reduce(lambda x,y: x or croniter.match(y, time), self.slideshow_timers, True)
        return is_enabled

