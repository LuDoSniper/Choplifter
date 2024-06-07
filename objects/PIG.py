# # PIG -> Python Image Generator
# # alias - le cochon

# import pytmx
# from PIL import Image

# def generate_map_image(tmx_file, output_image_file):
#     # Charger le fichier TMX
#     tmx_data = pytmx.TiledMap(tmx_file)

#     # Obtenir les dimensions de la carte et des tuiles
#     map_width = tmx_data.width
#     map_height = tmx_data.height
#     tile_width = tmx_data.tilewidth
#     tile_height = tmx_data.tileheight

#     # Créer une nouvelle image vide avec la taille de la carte
#     map_image = Image.new('RGBA', (map_width * tile_width, map_height * tile_height))

#     # Parcourir les couches de la carte
#     for layer in tmx_data.visible_layers:
#         if isinstance(layer, pytmx.TiledTileLayer):
#             for x, y, gid in layer:
#                 tile_info = tmx_data.get_tile_image_by_gid(gid)
#                 if tile_info:
#                     image_path, region, flags = tile_info
#                     tile_image = Image.open(image_path).crop((region[0], region[1], region[0] + region[2], region[1] + region[3]))
#                     print(f'Processing tile at ({x}, {y}) with gid {gid}')
#                     print(f'Tile region: {region}')
                    
#                     # Si la tuile a une couche alpha, utiliser un masque
#                     if tile_image.mode == 'RGBA':
#                         tile_mask = tile_image.split()[3]
#                         map_image.paste(tile_image, (x * tile_width, y * tile_height), tile_mask)
#                     else:
#                         map_image.paste(tile_image, (x * tile_width, y * tile_height))

#     # Sauvegarder l'image finale
#     map_image.save(output_image_file)

# # Exemple d'utilisation
# generate_map_image('assets/tilesets/survival/2-1.tmx', 'output_map.png')

import pytmx
from PIL import Image

def generate_map_image(tmx_file, output_image_file):
    # Charger le fichier TMX
    tmx_data = pytmx.TiledMap(tmx_file)

    # Obtenir les dimensions de la carte et des tuiles
    map_width = tmx_data.width
    map_height = tmx_data.height
    tile_width = tmx_data.tilewidth
    tile_height = tmx_data.tileheight

    # Créer une nouvelle image vide avec la taille de la carte
    map_image = Image.new('RGBA', (map_width * tile_width, map_height * tile_height))

    # Parcourir les couches de la carte
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile_info = tmx_data.get_tile_image_by_gid(gid)
                if tile_info:
                    image_path, region, flags = tile_info
                    left, upper, width, height = region
                    right = left + width
                    lower = upper + height
                    region = (left, upper, right, lower)
                    
                    # Ouvrir l'image de la tuile et la découper
                    tile_image = Image.open(image_path).crop(region)
                    # print(f'Processing tile at ({x}, {y}) with gid {gid}')
                    # print(f'Tile region: {region}')
                    
                    # Créer une image temporaire pour la tuile à la position correcte
                    temp_image = Image.new('RGBA', map_image.size)
                    temp_image.paste(tile_image, (x * tile_width, y * tile_height))

                    # Fusionner la tuile avec l'image de la carte en tenant compte de la transparence
                    map_image = Image.alpha_composite(map_image, temp_image)

    # Sauvegarder l'image finale
    map_image.save(output_image_file)

# Exemple d'utilisation
# generate_map_image('assets/tilesets/survival/2-1.tmx', 'output_map.png')