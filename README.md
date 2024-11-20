# Relatório de Execução do Programa - Escalonamento de Processos (Round Robin)

Este relatório descreve os eventos observados durante a execução de um programa de escalonamento de processos utilizando o algoritmo **Round Robin**. O programa realiza a execução de tarefas enquanto gerencia uma **Fila de Prontos (Ready Queue)** e uma **Fila de E/S (I/O Queue)**.

---

## **Descrição do Algoritmo**
O algoritmo de **Round Robin** é utilizado para escalonar processos, alternando entre eles em intervalos fixos de tempo, também conhecidos como *quantum*. Os processos que não completam sua execução dentro do *quantum* são colocados novamente na fila de prontos. Caso um processo entre em estado de E/S, ele é movido para a **Fila de E/S**.

---

## **Principais Eventos Durante a Execução**

1. **Processo P1 Inicia**
   - P1 começa com 3.0 segundos restantes.
   - Executa por 2 segundos (restando 1.0 segundo).
   - Após o término do *quantum*, P2 é iniciado.

2. **Processo P2 Inicia**
   - P2 começa com 2.0 segundos restantes.
   - Executa por 2 segundos (processo finalizado e entra em E/S).
   - P3 é iniciado.

3. **Processo P3 Inicia**
   - P3 começa com 1.0 segundo restante.
   - Executa por 1 segundo (processo finalizado e entra em E/S).
   - P1 é retomado.

4. **Retomada do Processo P1**
   - P1 executa os 1.0 segundo restantes.
   - Entra em E/S após concluir sua execução.

5. **Novos Ciclos de E/S e Execução**
   - P3 conclui sua operação de E/S e retorna para execução.
   - Após P3 finalizar, P2 e P1 reentram na fila para execução.
   - Ciclos de execução e E/S continuam até que todos os processos sejam finalizados.

---

## **Estados das Filas**
Durante a execução, as filas mantiveram os seguintes estados:

- **Fila de Prontos (Ready Queue):**
  Contém os processos prontos para execução, alternando entre P1, P2 e P3.
  
- **Fila de E/S (I/O Queue):**
  Contém os processos que aguardam a conclusão de operações de entrada/saída.

Exemplo de estados:
```plaintext
==== Estado das Filas ====
Fila de Prontos: ['P2', 'P3']
Fila de E/S: []
```

---

## **Visualização**
O programa gerou um gráfico que mostra o tempo de execução de cada processo ao longo do tempo. O gráfico utiliza blocos coloridos para representar os intervalos de execução de cada processo.
![Figure_1](https://github.com/user-attachments/assets/e600b9da-2e49-4c91-af7b-f8000b2fb22e)


---

## **Condições Finais**
Ao término da execução:
- Todos os processos (P1, P2 e P3) completaram suas tarefas.
- A **Fila de Prontos** ficou vazia.
- A **Fila de E/S** registrou os processos em seus respectivos períodos de espera.

---

## **Observações**
- A implementação demonstra corretamente o comportamento do algoritmo Round Robin.
- A alternância entre processos e o gerenciamento da E/S funcionaram conforme esperado.
- O gráfico final fornece uma boa representação visual do escalonamento.

