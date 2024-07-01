[app]
title = My Kivy App
package.name = mykivyapp
package.domain = org.test
source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = images/*, assets/*
version = 0.1
orientation = portrait
android.permissions = INTERNET
requirements = python3,kivy,Pillow,opencv-python-headless,numpy
icon.filename = assets/icon.png
presplash.filename = assets/splash.png
android.arch = armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
