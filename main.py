from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
import keyboard
import os
import pyautogui
from PIL import Image
import cv2
import numpy as np


def preprocess_image(image_path, save_path=None):
    image = Image.open(image_path).convert('L')
    image = np.array(image)
    if save_path:
        cv2.imwrite(save_path, image)
        print(f"Saved processed image to {save_path}")
    return image


def locate_button_on_screen(template_image, save_path=None):
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_BGR2GRAY)
    if save_path:
        cv2.imwrite(save_path, screen)
        print(f"Saved screenshot to {save_path}")
    res = cv2.matchTemplate(screen, template_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val >= 0.8:
        print(f"Button located at position {max_loc}")
        return max_loc
    else:
        print("Button not found")
    return None


class MyApp(App):
    def build(self):
        self.label = Label(text="Running script. Press 'Esc' to terminate.")
        Clock.schedule_interval(self.process_images, 1)
        return self.label

    def process_images(self, dt):
        processed_images_dir = "processed_images"
        screenshots_images_dir = "screenshots"
        click_screenshots_dir = "click_screenshots"
        os.makedirs(processed_images_dir, exist_ok=True)
        os.makedirs(screenshots_images_dir, exist_ok=True)
        os.makedirs(click_screenshots_dir, exist_ok=True)

        files = os.listdir("my_kivy_app/images")

        if keyboard.is_pressed("Esc"):
            self.stop()
            return

        main_screen = "click_screenshots/img.png"
        for f in files:
            picture = "my_kivy_app/images/" + f
            try:
                save_path = os.path.join(processed_images_dir, f)
                screenshots_path = os.path.join(screenshots_images_dir, f)
                print(f"Processing image: {picture}")
                template_image = preprocess_image(picture, save_path=save_path)
                button_location = locate_button_on_screen(template_image, save_path=screenshots_path)
                if button_location:
                    pyautogui.click(button_location)
                    pyautogui.sleep(1)
                    print("Clicked on the button")
            except Exception as e:
                print(f"Error processing image {picture}: {e}")


if __name__ == '__main__':
    MyApp().run()
