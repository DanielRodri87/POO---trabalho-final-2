import os
import abc
import time
from typing import List, Dict, Optional

# Funções utilitárias
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("Pressione Enter para continuar...")

# Classes de Autenticáveis e Pessoas
class Autenticavel(abc.ABC):
    @abc.abstractmethod
    def obter_permissoes(self):
        pass

class Pessoa:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

# Classes de Usuários
class Barbeiro(Pessoa, Autenticavel):
    def __init__(self, nome, cpf, salario):
        super().__init__(nome, cpf)
        self.horarios_livres = {
            "Segunda": [],
            "Terça": [],
            "Quarta": [],
            "Quinta": [],
            "Sexta": [],
            "Sábado": []
        }
        self.salario = salario

    def adicionar_horario_livre(self, dia, horario):
        if dia in self.horarios_livres:
            self.horarios_livres[dia].append(horario)
        else:
            raise ValueError("Dia inválido.")

    def remover_horario_livre(self, dia, horario):
        if dia in self.horarios_livres and horario in self.horarios_livres[dia]:
            self.horarios_livres[dia].remove(horario)
        else:
            raise ValueError("Horário não encontrado para o dia especificado.")

    def obter_permissoes(self):
        return ["listar_horarios", "reservar_horario", "listar_clientes", "editar_cliente", "excluir_cliente"]

class Cliente(Pessoa, Autenticavel):
    def __init__(self, nome, cpf, corte_desejado, valor, dia, horario_desejado):
        super().__init__(nome, cpf)
        self.corte_desejado = corte_desejado
        self.valor = valor
        self.dia = dia
        self.horario_desejado = horario_desejado

    def obter_permissoes(self):
        return ["listar_horarios", "reservar_horario"]

class Visitante(Pessoa):
    def __init__(self, nome, cpf):
        super().__init__(nome, cpf)

# Classe da Barbearia
class Barbearia:
    def __init__(self, barbeiro):
        self.barbeiro = barbeiro
        self.clientes = []

    def listar_horarios_disponiveis(self, dia):
        if dia in self.barbeiro.horarios_livres:
            return self.barbeiro.horarios_livres[dia]
        else:
            raise ValueError("Dia inválido.")

    def reservar_horario(self, cliente):
        if cliente.dia in self.barbeiro.horarios_livres and cliente.horario_desejado in self.barbeiro.horarios_livres[cliente.dia]:
            self.clientes.append(cliente)
            self.barbeiro.remover_horario_livre(cliente.dia, cliente.horario_desejado)
            return True
        return False

    def listar_clientes(self):
        return self.clientes

    def editar_cliente(self, cpf, **kwargs):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                cliente.nome = kwargs.get('nome', cliente.nome)
                cliente.corte_desejado = kwargs.get('corte_desejado', cliente.corte_desejado)
                cliente.valor = kwargs.get('valor', cliente.valor)
                cliente.dia = kwargs.get('dia', cliente.dia)
                cliente.horario_desejado = kwargs.get('horario_desejado', cliente.horario_desejado)
                return
        raise ValueError("Cliente não encontrado.")

    def excluir_cliente(self, cpf):
        self.clientes = [cliente for cliente in self.clientes if cliente.cpf != cpf]

# Classes de Cálculo de Salário
class CalcularSalarioBarbeiro:
    def __init__(self, barbeiro, clientes):
        self.barbeiro = barbeiro
        self.clientes = clientes

    def calcular_lucro(self):
        total = sum(cliente.valor for cliente in self.clientes)
        return total

    def verificar_lucro(self):
        return self.calcular_lucro() > self.barbeiro.salario

# Classes de Login e Cadastro
class Login:
    def __init__(self, usuarios):
        self.usuarios = usuarios

    def autenticar(self, cpf):
        return self.usuarios.get(cpf)

class Cadastrar:
    def __init__(self):
        self.usuarios = {}

    def cadastrar_barbeiro(self, nome, cpf, salario):
        if cpf in self.usuarios:
            raise ValueError("CPF já cadastrado.")
        barbeiro = Barbeiro(nome, cpf, salario)
        self.usuarios[cpf] = barbeiro

    def cadastrar_cliente(self, nome, cpf, corte_desejado, valor, dia, horario_desejado):
        if cpf in self.usuarios:
            raise ValueError("CPF já cadastrado.")
        cliente = Cliente(nome, cpf, corte_desejado, valor, dia, horario_desejado)
        self.usuarios[cpf] = cliente

    def cadastrar_visitante(self, nome, cpf):
        if cpf in self.usuarios:
            raise ValueError("CPF já cadastrado.")
        visitante = Visitante(nome, cpf)
        self.usuarios[cpf] = visitante

    def existe_barbeiro_cadastrado(self):
        return any(isinstance(usuario, Barbeiro) for usuario in self.usuarios.values())

# Funções de menu
def adicionar_horarios_barbeiro(barbeiro):
    dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
    for dia in dias_semana:
        while True:
            try:
                entrada = int(input(f"{dia} - Horário de entrada (0-23h): "))
                saida = int(input(f"{dia} - Horário de saída (0-23h): "))
                if 0 <= entrada <= 23 and 0 <= saida <= 23 and entrada <= saida:
                    break
                else:
                    print("Horário inválido. Por favor, insira um horário entre 0 e 23 e certifique-se de que a hora de entrada seja anterior ou igual à hora de saída.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")
        for hora in range(entrada, saida + 1):
            barbeiro.adicionar_horario_livre(dia, f"{hora}h")

def menu_corte():
    print("Escolha o tipo de corte:")
    print("1 - Americano: 15 reais")
    print("2 - Mullet: 15 reais")
    print("3 - Low Fade: 18 reais")
    print("4 - Social: 12 reais")
    try:
        opcao = int(input("Escolha uma opção: "))
        cortes = {
            1: ("Americano", 15),
            2: ("Mullet", 15),
            3: ("Low Fade", 18),
            4: ("Social", 12)
        }
        return cortes.get(opcao, ("Opção inválida", 0))
    except ValueError:
        return ("Opção inválida", 0)

def menu_dia():
    print("Escolha o dia:")
    print("1 - Segunda")
    print("2 - Terça")
    print("3 - Quarta")
    print("4 - Quinta")
    print("5 - Sexta")
    print("6 - Sábado")
    try:
        opcao = int(input("Escolha uma opção: "))
        dias = {
            1: "Segunda",
            2: "Terça",
            3: "Quarta",
            4: "Quinta",
            5: "Sexta",
            6: "Sábado"
        }
        return dias.get(opcao, "Opção inválida")
    except ValueError:
        return "Opção inválida"

def menu_horario(horarios):
    print("Escolha o horário:")
    for idx, horario in enumerate(horarios, 1):
        print(f"{idx} - {horario}")
    try:
        opcao = int(input("Escolha uma opção: "))
        if 1 <= opcao <= len(horarios):
            return horarios[opcao - 1]
        return "Opção inválida"
    except ValueError:
        return "Opção inválida"

# Inicialização do sistema
cadastrar = Cadastrar()
login = Login(cadastrar.usuarios)
barbearia = None

# Menu principal
while True:
    clear_screen()
    print("1 - Cadastrar barbeiro")
    print("2 - Cadastrar cliente")
    print("3 - Cadastrar visitante")
    print("4 - Fazer login")
    print("5 - Sair")
    try:
        opcao = int(input("Escolha uma opção: "))
    except ValueError:
        print("Opção inválida. Por favor, insira um número.")
        pause()
        continue

    if opcao == 1:
        clear_screen()
        nome = input("Nome: ")
        cpf = input("CPF: ")
        try:
            salario = float(input("Salário: "))
        except ValueError:
            print("Salário inválido. Por favor, insira um número.")
            pause()
            continue
        try:
            cadastrar.cadastrar_barbeiro(nome, cpf, salario)
            barbeiro = cadastrar.usuarios[cpf]
            adicionar_horarios_barbeiro(barbeiro)
        except ValueError as e:
            print(e)
        pause()

    elif opcao == 2:
        clear_screen()
        if not cadastrar.existe_barbeiro_cadastrado():
            print("Não há barbeiro cadastrado. Por favor, cadastre um barbeiro primeiro.")
            pause()
            continue
        nome = input("Nome: ")
        cpf = input("CPF: ")
        corte_desejado, valor = menu_corte()
        if corte_desejado == "Opção inválida":
            print(corte_desejado)
            pause()
            continue
        dia = menu_dia()
        if dia == "Opção inválida":
            print(dia)
            pause()
            continue
        try:
            if dia in barbeiro.horarios_livres:
                horario_desejado = menu_horario(barbeiro.horarios_livres[dia])
                if horario_desejado == "Opção inválida":
                    print(horario_desejado)
                    pause()
                    continue
                cadastrar.cadastrar_cliente(nome, cpf, corte_desejado, valor, dia, horario_desejado)
                cliente = cadastrar.usuarios[cpf]
                if barbearia is None:
                    barbearia = Barbearia(barbeiro)
                barbearia.reservar_horario(cliente)
            else:
                print("Dia inválido.")
        except ValueError as e:
            print(e)
        pause()

    elif opcao == 3:
        clear_screen()
        nome = input("Nome: ")
        cpf = input("CPF: ")
        try:
            cadastrar.cadastrar_visitante(nome, cpf)
        except ValueError as e:
            print(e)
        pause()

    elif opcao == 4:
        clear_screen()
        cpf = input("CPF: ")
        usuario = login.autenticar(cpf)
        if usuario is None:
            print("CPF não encontrado.")
            pause()
            continue
        permissoes = usuario.obter_permissoes()
        if isinstance(usuario, Barbeiro):
            while True:
                clear_screen()
                print("1 - Listar horários disponíveis")
                print("2 - Listar clientes")
                print("3 - Editar cliente")
                print("4 - Excluir cliente")
                print("5 - Calcular lucro")
                print("6 - Sair")
                try:
                    opcao = int(input("Escolha uma opção: "))
                except ValueError:
                    print("Opção inválida. Por favor, insira um número.")
                    pause()
                    continue

                if opcao == 1:
                    clear_screen()
                    dia = menu_dia()
                    if dia == "Opção inválida":
                        print(dia)
                        pause()
                        continue
                    horarios = barbearia.listar_horarios_disponiveis(dia)
                    print(f"Horários disponíveis em {dia}: {horarios}")
                    pause()

                elif opcao == 2:
                    clear_screen()
                    clientes = barbearia.listar_clientes()
                    for cliente in clientes:
                        print(f"Nome: {cliente.nome}, CPF: {cliente.cpf}, Corte: {cliente.corte_desejado}, Valor: {cliente.valor}, Dia: {cliente.dia}, Horário: {cliente.horario_desejado}")
                    pause()

                elif opcao == 3:
                    clear_screen()
                    cpf_cliente = input("CPF do cliente: ")
                    nome = input("Novo nome (deixe em branco para manter): ")
                    corte_desejado, valor = menu_corte()
                    if corte_desejado == "Opção inválida":
                        print(corte_desejado)
                        pause()
                        continue
                    dia = menu_dia()
                    if dia == "Opção inválida":
                        print(dia)
                        pause()
                        continue
                    horario_desejado = menu_horario(barbearia.listar_horarios_disponiveis(dia))
                    if horario_desejado == "Opção inválida":
                        print(horario_desejado)
                        pause()
                        continue
                    try:
                        barbearia.editar_cliente(cpf_cliente, nome=nome, corte_desejado=corte_desejado, valor=valor, dia=dia, horario_desejado=horario_desejado)
                    except ValueError as e:
                        print(e)
                    pause()

                elif opcao == 4:
                    clear_screen()
                    cpf_cliente = input("CPF do cliente: ")
                    try:
                        barbearia.excluir_cliente(cpf_cliente)
                    except ValueError as e:
                        print(e)
                    pause()

                elif opcao == 5:
                    clear_screen()
                    calculo_salario = CalcularSalarioBarbeiro(barbearia.barbeiro, barbearia.listar_clientes())
                    lucro = calculo_salario.calcular_lucro()
                    print(f"Lucro total: {lucro}")
                    print(f"Lucro excede o salário? {'Sim' if calculo_salario.verificar_lucro() else 'Não'}")
                    pause()

                elif opcao == 6:
                    break

        elif isinstance(usuario, Cliente):
            while True:
                clear_screen()
                print("1 - Listar horários disponíveis")
                print("2 - Reservar horário")
                print("3 - Sair")
                try:
                    opcao = int(input("Escolha uma opção: "))
                except ValueError:
                    print("Opção inválida. Por favor, insira um número.")
                    pause()
                    continue

                if opcao == 1:
                    clear_screen()
                    dia = menu_dia()
                    if dia == "Opção inválida":
                        print(dia)
                        pause()
                        continue
                    horarios = barbearia.listar_horarios_disponiveis(dia)
                    print(f"Horários disponíveis em {dia}: {horarios}")
                    pause()

                elif opcao == 2:
                    clear_screen()
                    corte_desejado, valor = menu_corte()
                    if corte_desejado == "Opção inválida":
                        print(corte_desejado)
                        pause()
                        continue
                    dia = menu_dia()
                    if dia == "Opção inválida":
                        print(dia)
                        pause()
                        continue
                    horario_desejado = menu_horario(barbearia.listar_horarios_disponiveis(dia))
                    if horario_desejado == "Opção inválida":
                        print(horario_desejado)
                        pause()
                        continue
                    try:
                        barbearia.reservar_horario(Cliente(usuario.nome, usuario.cpf, corte_desejado, valor, dia, horario_desejado))
                    except ValueError as e:
                        print(e)
                    pause()

                elif opcao == 3:
                    break

        elif isinstance(usuario, Visitante):
            clear_screen()
            print("Bem-vindo, visitante!")
            pause()

    elif opcao == 5:
        break
