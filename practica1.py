import threading
import queue
import time
import random

tiempo_inicio = time.time()

lista_documentos = []
for i in range(1, 25):
    lista_documentos.append({
        "id": f"DOC-{i:02d}", 
        "tamano": random.randint(1, 5)
    })

random.shuffle(lista_documentos)

cola_documentos = queue.Queue()
for doc in lista_documentos:
    cola_documentos.put(doc)

nombres_trabajadores = ['Carlos', 'Sofia', 'Mateo', 'Valentina']

registro_trabajadores = {nombre: [] for nombre in nombres_trabajadores}
lock_global = threading.Lock()

MAX_DOCS_POR_TRABAJADOR = 6

def trabajador(identificador):
    docs_procesados = 0
    
    while docs_procesados < MAX_DOCS_POR_TRABAJADOR:
        try:
            documento = cola_documentos.get_nowait()
        except queue.Empty:
            break
        
        time.sleep(documento["tamano"] * 0.1)
        
        with lock_global:
            registro_trabajadores[identificador].append(documento)
            docs_procesados += 1
            print(f"[{identificador:<9}] Proceso: {documento['id']} (Tamano: {documento['tamano']})  |  Avance: {docs_procesados}/6")
            
        cola_documentos.task_done()

if __name__ == "__main__":
    print("=" * 60)
    print("SIMULACION DE PROCESAMIENTO CONCURRENTE DE DOCUMENTOS")
    print("=" * 60 + "\n")
    
    hilos = []
    for nombre in nombres_trabajadores:
        hilo = threading.Thread(target=trabajador, args=(nombre,))
        hilos.append(hilo)
        hilo.start()
        
    for hilo in hilos:
        hilo.join()
        
    tiempo_total = time.time() - tiempo_inicio
    
    print("\n" + "=" * 60)
    print("RESUMEN GENERAL Y DETALLADO POR TRABAJADOR")
    print("=" * 60)
    
    total_procesados = 0
    for trab, docs in registro_trabajadores.items():
        cantidad = len(docs)
        total_procesados += cantidad
        tamano_acumulado = sum([d["tamano"] for d in docs])
        ids_docs = ", ".join([d["id"] for d in docs])
        
        print(f"\n* Trabajador: {trab} ({cantidad} documentos procesados)")
        print(f"  Tamano total acumulado: {tamano_acumulado} unidades")
        print(f"  Documentos asignados: {ids_docs}")
        
    print("\n" + "-" * 60)
    print(f"Total de documentos procesados en el sistema: {total_procesados} de 24")
    print(f"Tiempo total de procesamiento: {tiempo_total:.2f} segundos")
    print("=" * 60)