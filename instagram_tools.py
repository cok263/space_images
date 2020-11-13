from instabot import Bot


def upload_to_instagram(login, password, images_dir):
    bot = Bot()
    bot.login(username=login, password=password)
    images = os.listdir(images_dir)
    for image in images:
        bot.upload_photo(os.path.join(images_dir, image), caption="Nice pic!")
