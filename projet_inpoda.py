import json
import re
import matplotlib.pyplot as plt # pour afficher des graphiques
import tkinter as tk


# ouverture du fichier JSON

with open('versailles_tweets_100.json','r',encoding='utf-8') as json_file:
    data = json.load(json_file)
tweets = []


# CLASS PRINCIPAL

class Tweet:
    def __init__(self, auteur, text, hashtags=[], mentions=[]):
        self.auteur = auteur
        self.texte = re.sub("[^a-zA-z0-9 @&é\"\'(§è!çà)\-#°\^¨$*€¥ôÔùÙ‰%`@#£=≠±+:÷\\/…•.;∞¿?,≤≥><]", "", text, 0)
        try:
            self.hashtags = [i['tag'] for i in hashtags['hashtags']]
        except:
            self.hashtags = []
        try:
            self.mentions = [i['username'] for i in mentions['mentions']]
        except:
            self.mentions = []


    def get_auteur(self):
        print("Auteur.e du tweet :", self.auteur)
    

    def get_hashtags(self):
        if bool(self.hashtags):
            print("Hashtag(s) du tweet :", self.hashtags)
        else:
            print("Ce tweet ne contient pas de hashtags.")


    def get_mentions(self):
        if bool(self.mentions):
            print("Mention(s) du tweet :", self.mentions)
        else:
            print("Ce tweet ne contient pas de mentions.")


# ITERATIONS DE LA CLASSE PRINCIPALE

for tweet in data:
    try:
        tweets.append(Tweet(tweet['_id'], tweet['text'], tweet['entities'], tweet['entities']))
    except:
        tweets.append(Tweet(tweet['_id'], tweet['text']))


# FONCTIONS

def reset_zone_datterissage():
    """Supprime tout le text du fichier zone_d'atterissage.txt."""
    open("zone_atterissage.txt", "w").close()


def fill_zone_datterissage():
    """Remplit la zone d'atterissage avec tous les objets tweets de la liste de tweets."""
    reset_zone_datterissage()
    fic = open('zone_atterissage.txt', 'a')
    for tweet in tweets:
        fic.write(str(tweet.__dict__)+"\n")
    fic.close()


def get_top_k_hashtags(k):
    """Affiche le top k des hashtags les plus utilisé dans un bar chart."""
    temp = [x.hashtags for x in tweets]
    temp = [x for y in temp for x in y]
    temp2 = dict()
    for i in temp:
        if i not in temp2.keys():
            temp2[i] = 1
        else:
            temp2[i] += 1
    temp2 = list(map(list, temp2.items())) # transforme le dictionnaire temp en liste de listes
    for x in temp2:
        x[0], x[1] = x[1], x[0]
    temp2.sort(reverse = True)
    try:
        a = temp2[k]
        temp3 = [x[0] for x in temp2[:k]]
        temp4 = [y[1] for y in temp2[:k]]
        plt.bar(temp4, temp3)
        plt.xlabel("Hashtag")
        plt.ylabel("Nombre d'utilisation")
        plt.title("Top {} des hashtags les plus utilisés".format(k))
        plt.show()
    except:
        print("- Il n'y a pas", k, "hashtags différents. Essayer un nombre inférieur.")


def get_top_k_users(k):
    """Affiche le top k des utilisateurs ayant le plus posté dans un bar chart."""
    temp = [x.auteur for x in tweets]
    temp2 = dict()
    for i in temp:
        if i not in temp2.keys():
            temp2[i] = 1
        else:
            temp2[i] += 1
    temp2 = list(map(list, temp2.items())) # transforme le dictionnaire temp en liste de listes
    for x in temp2:
        x[0], x[1] = x[1], x[0]
    temp2.sort(reverse = True)
    try:
        a = temp2[k]
        temp3 = [x[0] for x in temp2[:k]]
        temp4 = [y[1] for y in temp2[:k]]
        plt.bar(temp4, temp3)
        plt.xlabel("Utilisateur")
        plt.ylabel("Nombre de posts")
        plt.title("Top {} des utilisateurs ayant le plus posté".format(k))
        plt.show()
    except:
        print("- Il n'y a pas", k, "utilisateurs différents. Essayer un nombre inférieur.")

def get_top_k_mentions(k):
    """Affiche le top k des utilisateurs les plus mentionné(e)s dans un bar chart."""
    temp = [x.mentions for x in tweets]
    temp = [x for y in temp for x in y]
    temp2 = dict()
    for i in temp:
        if i not in temp2.keys():
            temp2[i] = 1
        else:
            temp2[i] += 1
    temp2 = list(map(list, temp2.items())) # transforme le dictionnaire temp en liste de listes
    for x in temp2:
        x[0], x[1] = x[1], x[0]
    temp2.sort(reverse = True)
    try:
        a = temp2[k]
        temp3 = [x[0] for x in temp2[:k]]
        temp4 = [y[1] for y in temp2[:k]]
        plt.bar(temp4, temp3)
        plt.xlabel("Mention")
        plt.ylabel("Nombre d'utilisation")
        plt.title("Top {} des mentions les plus utilisées".format(k))
        plt.show()
    except:
        print("- Il n'y a pas", k, "utilisateurs mentionné(e)s différent(e)s. Essayer un nombre inférieur.")


def get_posts_per_user(user):
    """Affiche tous les tweets postés par l'utilisateur."""
    temp = []
    for tweet in tweets:
        if str(user) == tweet.auteur:
            temp.append(tweet)
    if bool(temp):
        print("- Voici l'ensemble des tweets de l'utilisateur", user, ":")
        for x in temp:
            print("    -", x.text)
    else:
        print("- L'utilisateur n'a pas tweeté ou le nom d'utilisateur est incorrect.")


def get_nb_posts_per_user(user):
    """Affiche le nombre de tweets postés par l'utilisateur."""
    temp = []
    for tweet in tweets:
        if str(user) == tweet.auteur:
            temp.append(tweet)
    if bool(temp):
        print("-", user, "a tweeté", len(temp), "fois.")
    else:
        print("- L'utilisateur n'a pas tweeté ou le nom d'utilisateur est incorrect.")


def get_nb_posts_per_hashtag(hashtag):
    """Affiche le nombre de tweet contenant le hashtag."""
    temp = []
    for tweet in tweets:
        if hashtag in tweet.hashtags:
            temp.append(tweet)
    if bool(temp):
        print("- Il y a", len(temp), "tweet(s) mentionnant le hashtag", hashtag, "\b.")
    else:
        print("- Il n'y a pas de tweet contenant le hashtag", hashtag, "\b.")


def get_posts_per_mention(mention):
    """Affiche les tweets contenant la mention."""
    temp = []
    for tweet in tweets:
        if mention in tweet.mentions:
            temp.append(tweet)
    if bool(temp):
        print("- Voici l'ensemble des tweets mentionnant", mention, ":")
        for x in temp:
            print("    -", x.text)
    else:
        print("- Il n'y a pas de tweet mentionnant", mention, "\b.")


def get_users_per_hashtag(hashtag):
    """Affiche les utilisateurs ayant utilisé le hashtag spécifié."""
    temp = []
    for tweet in tweets:
        if hashtag in tweet.hashtags:
            temp.append(tweet)
    if bool(temp):
        print("- Utilisateur(s) ayant utilisé le hashtag", hashtag, ":")
        for x in temp:
            print("    -", x.auteur)
    else:
        print("- Il n'y a pas d'utilisateur ayant utilisé le hashtag", hashtag, "\b.")


def get_mentions_per_user(user):
    """Affiche les mentions de l'utilisateur spécifié."""
    for tweet in tweets:
        if tweet.auteur == str(user):
            temp = tweet
    try:
        if len(temp) == 0:
            print("- L'utilisateur", user, "n'a fait aucune mention ou n'existe pas.")
        print("- Mention(s) de l'utilisateur", user, ":")
        for x in temp.mentions:
            print("    -", x)
    except:
        print("- L'utilisateur", user, "n'a fait aucune mention ou n'existe pas.")

#Console

fill_zone_datterissage()

print("- InPoDa")
print("- 1_ Afficher le top k des hashtags les plus utilisés.")
print("- 2_ Afficher le top k des utilisateurs ayant le plus posté.")
print("- 3_ Afficher le top k des mentions les plus utilisés.")
print("- 4_ Afficher le nombre de posts d'un utilisateur.")
print("- 5_ Afficher le nombre de posts contenant un hashtag.")
print("- 6_ Afficher les posts d'un utilisateur.")
print("- 7_ Afficher les posts contenant une mention.")
print("- 8_ Afficher les utilisateurs ayant utilisé un hashtag.")
print("- 9_ Afficher les mentions d'un utilisateur.")

x=input('commande choisie: ')
if x == "1":
     print("- Affichage du top k des hashtags les plus utilisés.")
     k = input("> Valeur de k : ")
     get_top_k_hashtags(int(k))
if x == "2":
     print("- Affichage du top k des utilisateurs ayant le plus posté.")
     k = input("> Valeur de k : ")
     get_top_k_users(int(k))
if x == "3":
        print("- Affichage du top k des mentions les plus utilisés.")
        k = input("> Valeur de k : ")
        get_top_k_mentions(int(k))
if x == "4":
     print("- Affichage du nombre de posts d'un utilisateur.")
     k = input("> Nom de l'utilisateur : ")
     get_nb_posts_per_user(k)
if x == "5":
        print("- Affichage du nombre de posts contenant un hashtag.")
        k = input("> Hashtag cherché : ")
        get_nb_posts_per_hashtag(k)
if x == "6":
     print("- Affichage des posts d'un utilisateur.")
     k = input("> Nom de l'utilisateur : ")
     get_posts_per_user(k)
if x == "7":
     print("- Affichage des posts contenant une mention.")
     k = input("> Mention cherché : ")
     get_posts_per_mention(k)
if x == "8":
     print("- Affichage des utilisateurs ayant utilisé un hashtag.")
     k = input("> Hashtag cherché : ")
     get_users_per_hashtag(k)
if x == "9":
     print("- Affichage des mentions d'un utilisateur.")
     k = input("> Utilisateur cherché : ")
     get_mentions_per_user(k)