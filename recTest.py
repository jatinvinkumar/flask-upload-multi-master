from selenium import webdriver
from PIL import Image
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('http://35.232.44.3:8080/ipfs/QmQ5nusUzBAeS3YGBnYroimd2jcQRYXvDZMj9c72D83Hxn/')

element = driver.find_element_by_tag_name("canvas")
location = element.location
size = element.size

driver.save_screenshot("imageCache/shot.png")



# x = location['x']
# y = location['y']
# w = size['width']
# h = size['height']
# width = x + w
# height = y + h

#im = Image.open('shot.png')
#im = im.crop((int(x), int(y), int(width), int(height)))
#im.save('image.png')