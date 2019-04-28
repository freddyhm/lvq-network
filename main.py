from system import System
import sys
import os

# need this so we can create python executable
path = getattr(sys, '_MEIPASS', os.getcwd())
os.chdir(path)

print("////////////////////////////////////////////////////////////")
print("/// Bievenue au super LVQ de Sebastien et Freddy! ///")
print("////////////////////////////////////////////////////////////")
print("")
print("Pour construire le reseau a partir du fichier de configuration [1]:")
print("Pour quitter le programme [2]: ")
user_choice = input("Entrer votre choix: ")

learned_already = 0

if user_choice == '1':
    print("Configuration du reseau...")
    system = System()
    system.build()

    while True:

        print("")
        print("")
        if learned_already == 0:
            print("Pour commencer apprentissage [1]")
        else:
            print("Pour commencer l\'apprentissage [1]")
            print("Pour commencer validation croise [2]")
            print("Pour commencer generalisation [3]")
            print("Pour sauvegarder l\'etat du reseau (tres lent!) [4]")
            print("Pour sauvegarder performance seulement (tres vite!) [5]")

        user_choice = input("Entrer votre choix:")

        if user_choice == '1':
            learned_already = 1
            system.run("learn")
        elif learned_already == 1 and user_choice == '2':
            system.run("vc")
        elif learned_already == 1 and user_choice == '3':
            system.run("generalization")
        elif learned_already == 1 and user_choice == '4':
            print("Sauvegarde du reseau en cours:")
            system.save()
            print("")
        elif learned_already == 1 and user_choice == '5':
            print("Sauvegarde de la performance en cours:")
            system.save_performance()
            print("Performance sauvegarder au fichier 'performance_output.txt'!")
            print("")

elif user_choice == '2':
    sys.exit()