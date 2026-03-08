from PIL import Image      # Pour ouvrir et modifier des images
import numpy as np         # Pour manipuler les pixels sous forme de tableau

def texte_en_bits(texte):
    """
    Transforme une chaîne de caractères en une chaîne binaire.
    Chaque caractère est converti en 8 bits (ex : 'A' devient '01000001').
    """
    return ''.join(f"{ord(c):08b}" for c in texte)

def cacher_message(image_entree, image_sortie, message):
    """
    Cache un message texte dans une image PNG.
    
    Le message est converti en binaire, puis chaque bit est caché dans 
    le bit de poids faible du canal rouge des pixels de l’image.

    - image_entree : nom du fichier image d’origine (ex : 'chat.png')
    - image_sortie : nom du fichier image modifiée (ex : 'chat_cache.png')
    - message : le texte qu’on veut cacher dans l’image
    """
    image = Image.open(image_entree)        # Ouvre l’image
    image = image.convert("RGB")            # On s’assure qu’elle est en couleur (3 canaux : R, G, B)
    pixels = np.array(image)                # Transforme l’image en tableau de pixels

    message_binaire = texte_en_bits(message) + '1111111111111110'  # On ajoute un marqueur de fin
    pixels_aplatis = pixels.reshape(-1, 3)   # On transforme l’image en liste de triplets [R, G, B]

    if len(message_binaire) > len(pixels_aplatis):
        raise ValueError("Le message est trop long pour être caché dans cette image.")

    # On remplace le bit de poids faible du rouge de chaque pixel par un bit du message
    for i, bit in enumerate(message_binaire):
        pixels_aplatis[i][0] = (pixels_aplatis[i][0] & 254) | int(bit)

    pixels_modifies = pixels_aplatis.reshape(pixels.shape)  # On remet le tableau dans sa forme d’origine
    image_modifiee = Image.fromarray(pixels_modifies.astype('uint8'))  # On crée une nouvelle image
    image_modifiee.save(image_sortie)  # On sauvegarde l’image avec le message caché



# Fonction inverse : Lire un message caché 

def bits_en_texte(bits):
    """
    Transforme une chaîne de bits (ex : '01000001') en texte.
    On découpe en blocs de 8 bits pour chaque caractère ASCII.
    """
    octets = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join([chr(int(octet, 2)) for octet in octets])

def get_msg(image_path):
    """
    Extrait un message caché dans une image en lisant les bits de poids faible du rouge.

    - image_path : chemin de l’image contenant le message (ex : 'chat_cache.png')

    Retourne : le message texte caché dans l’image.
    """
    image = Image.open(image_path)
    image = image.convert("RGB")
    pixels = np.array(image)
    pixels_aplatis = pixels.reshape(-1, 3)

    bits = ''
    for pixel in pixels_aplatis:
        bits += str(pixel[0] & 1)  # On récupère le bit de poids faible du rouge
        if bits.endswith('1111111111111110'):  # Si on détecte le marqueur de fin, on arrête
            break

    return bits_en_texte(bits[:-16])  # On enlève le marqueur avant de traduire

message = get_msg("image_changee.png")
print("Message caché : ", message)


# ------

if __name__ == "__main__":
    image_originale = "image1.png"      
    image_trafiquee = "image_changee.png"
    message_secret = "Bonjour, je suis Abdallah Remmide et j'ai developpé deux outils de stéganographie permettant de cacher et lire des messages dans une image"

    print("1. Dissimulation du message en cours...")
    cacher_message(image_originale, image_trafiquee, message_secret)
    print(f"Message caché avec succès dans '{image_trafiquee}'.\n")

    print("2. Extraction du message en cours...")
    message_retrouve = get_msg(image_trafiquee)
    print("Voici le message extrait :")
    print("-->", message_retrouve)