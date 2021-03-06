import os
sprites= 'GameArt/Sprites/'
music = 'GameArt/Music/'
songs = music+"Songs/"
menu = sprites+"Menu/"
player = sprites+"Player/"
expl = sprites+"Explotion/"
background = 'GameArt/Sprites/dark1.jpg'
background2 = sprites+"black.png"
space_fuel = player+"space_fuel.png"
asteroids = [sprites+"aestroid1.png", sprites+"aestroid2.png", sprites+"aestroid3.png", sprites+"aestroid4.png",
             space_fuel, sprites+"Meteor_01.png", sprites+"Meteor_02.png",
             sprites+"Meteor_03.png", sprites+"Meteor_04.png"]
spaceship = [player+str(x)+".png" for x in range(1, 9)]
bullet = sprites+"bullet_red.png"

background_songs = [songs+"best of me(neffex).mp3", songs+"closer(neffex).mp3", songs+"crown(neffex).mp3",
                    songs+"life(neffex).mp3", songs+"starsky(tsfh).mp3", songs+"rumors(neffex).mp3"]

bullet_sound = music+"bullet.wav"
coin_collect = music+"coin_collect.wav"
menu_items = [menu+"play.png", menu+"options.png", menu+"credit.png", menu+ "exit.png"]
hover = music+"hover.wav"
hit = music +"hit.wav"
explosions = [expl+"Explosion1_"+str(x)+".png" for x in range(1, 12)]
explosions_bricks = [expl+"break1.png", expl+"break2.png", expl+"break3.png"]
explosion_sound = music+"explosion.wav"
explosion_sound2 = music+"explosion2.wav"

fonts = ['GameArt/Fonts/font1.ttf', 'GameArt/Fonts/font2.ttf']
levelBuild = 'GameArt/Sprites/levelBuilder/'
enemies = 'GameArt/Sprites/Enemies/'
bricks = [levelBuild+"spacebrick.jpg", levelBuild+"spacebrick2.jpg",
          levelBuild+"spacebrick3.jpg", levelBuild+"pass_through.png"]
objects = [levelBuild+"object1.jpg", levelBuild+"object2.jpg", levelBuild+"object3.jpg", levelBuild+"score.png",
           levelBuild+'bold_silver.png', levelBuild+'shield_silver.png', levelBuild+"key.png",
           levelBuild+"pass_through.png"]
enemies = [enemies+"enemy"+str(x)+".png" for x in range(1, 5)]
enem_bullet = ['GameArt/Sprites/Enemies/enemyBullet.png', 'GameArt/Sprites/Enemies/enemBullet2.png' ]
enemy_path = 'GameArt/Sprites/Enemies/'
random_enemies = [enemy_path+"random1.png", enemy_path+"random2.png", enemy_path+"random3.png", enemy_path+"random4.png"]

