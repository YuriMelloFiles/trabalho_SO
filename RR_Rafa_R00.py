import threading
import queue
import time
from datetime import datetime, timezone
import matplotlib.pyplot as plt



# Lista para armazenar as informações de tempo de cada tarefa
task_times = []

# Função que simula I/O
def process_task_io(name, duration):
    """
    Simula um processo I/O-bound.

    Args:
        name (str): Nome do processo.
        duration (int): Tempo total necessário para o processo (em segundos).
    """
    start_time_io = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"\033[33m[{start_time_io}]--Processo {name} iniciou E/S (PID: {threading.get_ident()}).\033[0m ")
    
    time.sleep(duration)  # Simula o tempo de espera para o processo I/O
    end_time_io = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"\033[32m[{end_time_io}]--Processo {name} concluiu E/S após {duration} segundos (PID: {threading.get_ident()}).\033[0m ")

# Função que simula o trabalho de um processo
def process_task(name, duration, quantum_time):
    start_time = datetime.now(timezone.utc)
    print(f"\033[36m[{start_time}] **... Processo {name} iniciou com {duration} segundos restantes (PID: {threading.get_ident()}) ...**\033[0m")

    time_to_run = min(duration, quantum_time)
    time.sleep(time_to_run)

    tempo_restante = duration - time_to_run
    end_time = datetime.now(timezone.utc)
    print(f"\033[32m[{end_time}] Processo {name} executou por {time_to_run} segundos. Restante: {tempo_restante} segundos (PID: {threading.get_ident()})\033[0m")
    
    # Armazena os tempos de início e término de cada tarefa
    task_times.append({"name": name, "start": start_time, "end": end_time})
    
    return tempo_restante

# Função que gerencia as threads, escolhendo o primeiro da fila
def thread_worker(queue, quantum_time, lock, io_queue):
    while True:
        with lock:
            if not queue.empty():
                current_process = queue.get()

                if current_process["Qtd_executions"] == 0:
                    # 1º execução antes da Entrada/Saída
                    first_execution = current_process["duration"]/2
                    tempo_restante = process_task(current_process["name"], first_execution, quantum_time)
                    current_process["Qtd_executions"] = 1
                else:
                    tempo_restante = process_task(current_process["name"], current_process["duration"], quantum_time)

                # Se o processo não terminou, insira ele novamente na fila com o tempo restante
                if tempo_restante > 0:
                    current_process["duration"] = tempo_restante
                    queue.put(current_process)
            else:
                break
        if current_process["io_made"] == False and tempo_restante == 0:
            io_queue.put(current_process)
            process_task_io(current_process["name"], current_process["I/O"])
            current_process["io_made"] = True
            current_process["Qtd_executions"] = 0
            current_process["duration"] = current_process["duration_backup"]
            queue.put(current_process)

# Função para plotar o gráfico de Gantt
def plot_gantt():
    # Converte os tempos de início e fim para uma escala de tempo que possa ser plotada
    names = [task["name"] for task in task_times]
    start_times = [task["start"] for task in task_times]
    end_times = [task["end"] for task in task_times]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Adiciona as barras para cada tarefa no gráfico
    for i, name in enumerate(names):
        ax.barh(name, (end_times[i] - start_times[i]).total_seconds(), left=(start_times[i] - min(start_times)).total_seconds())

    ax.set_xlabel("Tempo (segundos)")
    ax.set_ylabel("Tarefas")
    ax.set_title("Escalonamento de Processos (Round Robin)")
    plt.show()

if __name__ == "__main__":
    lock = threading.Lock()
    processes = [
        {"name": "P1", "duration": 6 , "I/O": 2 , "Qtd_executions": 0 , "io_made": False, "duration_backup": 6 , "io_type": "Disco"},
        {"name": "P2", "duration": 4, "I/O": 3, "Qtd_executions": 0, "io_made": False ,  "duration_backup": 4 , "io_type": "Fita"}, 
        {"name": "P3", "duration": 2, "I/O": 1, "Qtd_executions": 0, "io_made": False ,  "duration_backup": 2 , "io_type": "Impressora"},
    ]

    fila_Um_quantum = 2  # Tempo de quantum 2 , alta prioridade
    fila_Dois_quantum = 4 # baixa prioridade

    ready_queue = queue.Queue()
    for p in processes:
        ready_queue.put(p)

    io_queue = queue.Queue()

    num_threads = 3
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=thread_worker, args=(ready_queue, fila_Um_quantum, lock, io_queue), name=f"Thread-{i+1}")
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Chama a função para plotar o gráfico de Gantt
    plot_gantt()

    final_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"\033[32m[{final_time}] Todos os processos foram concluidos.\033[0m")