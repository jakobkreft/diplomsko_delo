'''
Ta program se uporablja za usklajevanje slike z drugim pogledom, tako da se objekti na sliki med seboj uskladijo.

Ukaz za zagon: python3 register.py ciljna_slika.png izvorna_slika.png
'''

import sys
import cv2
from selectors import DefaultSelector
import numpy as np


correct_img_name = 'frame3422.jpg'
incorrect_img_name = 'frame3422.jpg'

file_location = "C:\\Users\\Segaplu\\Desktop\\S\\diplomska\\posnetki"
teren = "\\teren6AB"
testnameA = "\\testA675803\\"
testnameB = "\\testB623652\\"
testnameB_aligned = "\\testB623652_aligned\\"


correct_img = cv2.imread(file_location + teren + testnameA +correct_img_name)
incorrect_img = cv2.imread(file_location + teren+ testnameB +incorrect_img_name)

# uporaba algoritma sift za odkrivanje značilnosti na slikah
sift_algorithm = cv2.SIFT_create()

# ustvari ključne točke
key_points_correct_image, descriptors_correct_image = sift_algorithm.detectAndCompute(correct_img, None)
key_points_incorrect_image, descriptors_incorrect_image = sift_algorithm.detectAndCompute(incorrect_img, None)

# nariši ključne točke na sliki
correct_img_keypoints = cv2.drawKeypoints(correct_img, key_points_correct_image, correct_img)
incorrect_img_keypoints = cv2.drawKeypoints(incorrect_img, key_points_incorrect_image, incorrect_img)

# Poglejmo, katere ključne točke izvirne slike so prisotne na sliki videoposnetka
# ujemanje značilnosti med videoposnetkom in statično sliko (uporaba algoritma flann za ujemanje značilnosti, ker je hitrejši od detektorja ORB match)
index_params = dict(algorithm = 0, trees = 5)
search_params = dict()

flann_algorithm = cv2.FlannBasedMatcher(index_params, search_params)

# poišči ujemanja z uporabo algoritma flann. Vračanje k najboljših ujemanj za vsako ključno točko.
matches = flann_algorithm.knnMatch(descriptors_correct_image, descriptors_incorrect_image, k=2)

# upoštevamo samo dobre ujemanja
good_matches = []

# iteriraj čez obe sliki m - izvirna, n - siv okvir
for m, n in matches:
    # določanje, kako dobro je ujemanje z primerjanjem razdalj.
    # manjša kot je razdalja, boljše je
    if m.distance < 0.5*n.distance:
        good_matches.append(m)

# nariši ujemanja med ključnimi točkami
# Opomba: Zloži dve sliki vodoravno in nariši črte od prve slike do druge slike, prikazuje najboljše ujemanje.
# Obstaja tudi cv2.drawMatchesKnn, ki nariše vseh k najboljših ujemanj. Če je k=2, bo narisal dve ujemalni črti za vsako ključno točko.
img3 = cv2.drawMatches(correct_img, key_points_correct_image, incorrect_img, key_points_incorrect_image, good_matches, incorrect_img)

# pridobi točke iz slovarja z dobrimi ujemanji
query_pts = np.float32([key_points_correct_image[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
train_pts = np.float32([key_points_incorrect_image[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

# uporaba algoritma RANSAC za iskanje homografije z odstranjenimi izvzetki.
homography_matrix, mask = cv2.findHomography(train_pts, query_pts, cv2.RANSAC, 5.0)

# Popači izvorno sliko do destinacije na podlagi homografije
# to storite za vse druge slike v mapi
number_of_frames = 7509
for i in range(1,number_of_frames+1):
    imgname = "frame" + str(i) + ".jpg"
    incorrect_img = cv2.imread(file_location+ teren + testnameB +imgname)

    im_out = cv2.warpPerspective(incorrect_img, homography_matrix, (correct_img.shape[1],correct_img.shape[0]))

    # shrani usklajeno sliko
    cv2.imwrite(file_location+  teren + testnameB_aligned +imgname, im_out)

    print ("Slika " + imgname + " je usklajena")
