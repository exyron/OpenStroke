import yaml


def testear_plantillas():
    with open("gestos.yaml", "r", encoding="utf-8") as f:
        datos = yaml.safe_load(f)
        plantillas = datos.get('plantillas', {})

        print(f"--- ANALIZANDO {len(plantillas)} PLANTILLAS ---")
        for nombre, puntos in plantillas.items():
            longitud = len(puntos)
            print(f"Gesto '{nombre}': {longitud} puntos.")
            if longitud != 64:
                print(f"  ⚠️ AVISO: El gesto '{nombre}' no tiene 64 puntos. Necesitará conversión.")
            else:
                print(f"  ✅ Gesto '{nombre}' compatible.")


if __name__ == "__main__":
    testear_plantillas()