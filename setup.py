from typing import List, Dict, Optional
from datetime import datetime, timedelta

class Pessoa:
    def __init__(self, nome: str, cpf: str):
        self.nome = nome
        self.cpf = cpf

class Barbeiro(Pessoa):
    def __init__(self, nome: str, cpf: str, salario: float):
        super().__init__(nome, cpf)
        self.horarios_livres: Dict[str, List[str]] = {
            "Segunda": [],
            "Terça": [],
            "Quarta": [],
            "Quinta": [],
            "Sexta": [],
            "Sábado": []
        }
        self.salario = salario

    def adicionar_horario_livre(self, dia: str, horario: str):
        if dia in self.horarios_livres:
            self.horarios_livres[dia].append(horario)
        else:
            raise ValueError("Dia inválido.")

    def remover_horario_livre(self, dia: str, horario: str):
        if dia in self.horarios_livres and horario in self.horarios_livres[dia]:
            self.horarios_livres[dia].remove(horario)
        else:
            raise ValueError("Horário não encontrado para o dia especificado.")

class Cliente(Pessoa):
    def __init__(self, nome: str, cpf: str, corte_desejado: str, valor: float, dia: str, horario_desejado: str):
        super().__init__(nome, cpf)
        self.corte_desejado = corte_desejado
        self.valor = valor
        self.dia = dia
        self.horario_desejado = horario_desejado

class Barbearia:
    def __init__(self, barbeiro: Barbeiro):
        self.barbeiro = barbeiro
        self.clientes: List[Cliente] = []

    def listar_horarios_disponiveis(self, dia: str) -> List[str]:
        if dia in self.barbeiro.horarios_livres:
            return self.barbeiro.horarios_livres[dia]
        else:
            raise ValueError("Dia inválido.")

    def reservar_horario(self, cliente: Cliente) -> bool:
        if cliente.dia in self.barbeiro.horarios_livres and cliente.horario_desejado in self.barbeiro.horarios_livres[cliente.dia]:
            self.clientes.append(cliente)
            self.barbeiro.remover_horario_livre(cliente.dia, cliente.horario_desejado)
            return True
        return False

    def listar_clientes(self) -> List[Cliente]:
        return self.clientes

    def editar_cliente(self, cpf: str, **kwargs):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                cliente.nome = kwargs.get('nome', cliente.nome)
                cliente.corte_desejado = kwargs.get('corte_desejado', cliente.corte_desejado)
                cliente.valor = kwargs.get('valor', cliente.valor)
                cliente.dia = kwargs.get('dia', cliente.dia)
                cliente.horario_desejado = kwargs.get('horario_desejado', cliente.horario_desejado)
                return
        raise ValueError("Cliente não encontrado.")

    def excluir_cliente(self, cpf: str):
        self.clientes = [cliente for cliente in self.clientes if cliente.cpf != cpf]

def adicionar_horarios_barbeiro(barbeiro: Barbeiro):
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
    for dia in dias_semana:
        while True:
            entrada = int(input(f"{dia} - Horário de entrada (0-23h): "))
            saida = int(input(f"{dia} - Horário de saída (0-23h): "))
            if 0 <= entrada <= 23 and 0 <= saida <= 23 and entrada <= saida:
                break
            else:
                print("Horário inválido. Por favor, insira um horário entre 0 e 23 e certifique-se de que a hora de entrada seja anterior ou igual à hora de saída.")
        for hora in range(entrada, saida + 1):
            barbeiro.adicionar_horario_livre(dia, f"{hora}h")

def menu_corte() -> str:
    print("Escolha o tipo de corte:")
    print("1 - Americano")
    print("2 - Mullet")
    print("3 - Low Fade")
    print("4 - Social")
    opcao = int(input("Escolha uma opção: "))
    cortes = {
        1: "Americano",
        2: "Mullet",
        3: "Low Fade",
        4: "Social"
    }
    return cortes.get(opcao, "Opção inválida")

cpfs_clientes = set()
cpfs_barbeiros = set()
barbearia = None

while True:
    print("1 - Cadastrar barbeiro")
    print("2 - Cadastrar cliente")
    print("3 - Listar horários disponíveis")
    print("4 - Reservar horário")
    print("5 - Listar clientes")
    print("6 - Editar cliente")
    print("7 - Excluir cliente")
    print("8 - Sair")
    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        nome = input("Nome: ")
        cpf = input("CPF: ")
        if cpf in cpfs_barbeiros or cpf in cpfs_clientes:
            print("CPF já cadastrado.")
            continue
        salario = float(input("Salário: "))
        barbeiro = Barbeiro(nome, cpf, salario)
        adicionar_horarios_barbeiro(barbeiro)
        barbearia = Barbearia(barbeiro)
        cpfs_barbeiros.add(cpf)
        
    elif opcao == 2:
        if not barbearia:
            print("Cadastre um barbeiro primeiro.")
            continue
        nome = input("Nome: ")
        cpf = input("CPF: ")
        if cpf in cpfs_barbeiros or cpf in cpfs_clientes:
            print("CPF já cadastrado.")
            continue
        corte_desejado = menu_corte()
        if corte_desejado == "Opção inválida":
            print("Opção de corte inválida.")
            continue
        valor = float(input("Valor: "))
        dia = input("Dia: ")
        horario_desejado = input("Horário desejado: ")
        cliente = Cliente(nome, cpf, corte_desejado, valor, dia, horario_desejado)
        cpfs_clientes.add(cpf)
        
    elif opcao == 3:
        if not barbearia:
            print("Cadastre um barbeiro primeiro.")
            continue
        print("Dias disponíveis:\n1 - Segunda\n2 - Terça\n3 - Quarta\n4 - Quinta\n5 - Sexta\n6 - Sábado\n7 - Cancelar")
        dia = int(input("Escolha um dia: "))
        if dia == 1:
            dia = "Segunda"
        elif dia == 2:
            dia = "Terça"
        elif dia == 3:
            dia = "Quarta"
        elif dia == 4:
            dia = "Quinta"
        elif dia == 5:
            dia = "Sexta"
        elif dia == 6:
            dia = "Sábado"
        elif dia == 7:
            continue
        else:
            print("Opção inválida.")
            continue
        
        print(barbearia.listar_horarios_disponiveis(dia))
        
    elif opcao == 4:
        if not barbearia:
            print("Cadastre um barbeiro primeiro.")
            continue
        if barbearia.reservar_horario(cliente):
            print("Horário reservado com sucesso.")
        else:
            print("Horário indisponível.")
            
    elif opcao == 5:
        if not barbearia:
            print("Cadastre um barbeiro primeiro.")
            continue
        for cliente in barbearia.listar_clientes():
            print(cliente.nome)
            
    elif opcao == 6:
        if not barbearia:
            print("Cadastre um barbeiro primeiro.")
            continue
        cpf = input("CPF do cliente: ")
        nome = input("Nome: ")
        corte_desejado = input("Corte desejado: ")
        valor = float(input("Valor: "))
        dia = input("Dia: ")
        horario_desejado = input("Horário desejado: ")
        barbearia.editar_cliente(cpf, nome=nome, corte_desejado=corte_desejado, valor=valor, dia=dia, horario_desejado=horario_desejado)
        
    elif opcao == 7:
        if not barbearia:
            print("Cadastre um barbeiro primeiro.")
            continue
        cpf = input("CPF do cliente: ")
        barbearia.excluir_cliente(cpf)
        cpfs_clientes.remove(cpf)
        
    elif opcao == 8:
        break
    
    print()
