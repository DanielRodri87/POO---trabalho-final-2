import abc
from typing import List, Dict, Optional

class Autenticavel(abc.ABC):
    @abc.abstractmethod
    def obter_permissoes(self):
        pass

class Pessoa:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf

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

class CalcularSalarioBarbeiro:
    def __init__(self, barbeiro, clientes):
        self.barbeiro = barbeiro
        self.clientes = clientes

    def calcular_lucro(self):
        total = sum(cliente.valor for cliente in self.clientes)
        return total

    def verificar_lucro(self):
        return self.calcular_lucro() > self.barbeiro.salario

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

def adicionar_horarios_barbeiro(barbeiro):
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

def menu_corte():
    print("Escolha o tipo de corte:")
    print("1 - Americano: 15 reais")
    print("2 - Mullet: 15 reais")
    print("3 - Low Fade: 18 reais")
    print("4 - Social: 12 reais")
    opcao = int(input("Escolha uma opção: "))
    cortes = {
        1: ("Americano", 15),
        2: ("Mullet", 15),
        3: ("Low Fade", 18),
        4: ("Social", 12)
    }
    return cortes.get(opcao, ("Opção inválida", 0))

def menu_dia():
    print("Escolha o dia:")
    print("1 - Segunda")
    print("2 - Terça")
    print("3 - Quarta")
    print("4 - Quinta")
    print("5 - Sexta")
    print("6 - Sábado")
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

def menu_horario(horarios):
    print("Escolha o horário:")
    for idx, horario in enumerate(horarios, 1):
        print(f"{idx} - {horario}")
    opcao = int(input("Escolha uma opção: "))
    if 1 <= opcao <= len(horarios):
        return horarios[opcao - 1]
    return "Opção inválida"

cadastrar = Cadastrar()
login = Login(cadastrar.usuarios)
barbearia = None

while True:
    print("1 - Cadastrar barbeiro")
    print("2 - Cadastrar cliente")
    print("3 - Cadastrar visitante")
    print("4 - Fazer login")
    print("5 - Sair")
    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        nome = input("Nome: ")
        cpf = input("CPF: ")
        salario = float(input("Salário: "))
        cadastrar.cadastrar_barbeiro(nome, cpf, salario)
        barbeiro = cadastrar.usuarios[cpf]
        adicionar_horarios_barbeiro(barbeiro)
        barbearia = Barbearia(barbeiro)
        
    elif opcao == 2:
        nome = input("Nome: ")
        cpf = input("CPF: ")
        cadastrar.cadastrar_cliente(nome, cpf, "", 0, "", "")
        
    elif opcao == 3:
        nome = input("Nome: ")
        cpf = input("CPF: ")
        cadastrar.cadastrar_visitante(nome, cpf)
        
    elif opcao == 4:
        cpf = input("CPF: ")
        usuario_autenticado = login.autenticar(cpf)
        if not usuario_autenticado:
            print("Usuário não encontrado.")
            continue

        if isinstance(usuario_autenticado, Barbeiro):
            while True:
                print("1 - Listar horários disponíveis")
                print("2 - Reservar horário")
                print("3 - Listar clientes")
                print("4 - Editar cliente")
                print("5 - Excluir cliente")
                print("6 - Calcular lucro")
                print("7 - Sair")
                opcao_usuario = int(input("Escolha uma opção: "))

                if opcao_usuario == 1:
                    dia = menu_dia()
                    if dia != "Opção inválida":
                        horarios = barbearia.listar_horarios_disponiveis(dia)
                        print(f"Horários disponíveis para {dia}: {horarios}")

                elif opcao_usuario == 2:
                    nome_cliente = input("Nome do cliente: ")
                    cpf_cliente = input("CPF do cliente: ")
                    dia = menu_dia()
                    if dia == "Opção inválida":
                        print("Opção de dia inválida.")
                        continue
                    horarios = barbearia.listar_horarios_disponiveis(dia)
                    horario_desejado = menu_horario(horarios)
                    if horario_desejado == "Opção inválida":
                        print("Opção de horário inválida.")
                        continue
                    corte_desejado, valor = menu_corte()
                    if corte_desejado == "Opção inválida":
                        print("Opção de corte inválida.")
                        continue
                    cliente = Cliente(nome_cliente, cpf_cliente, corte_desejado, valor, dia, horario_desejado)
                    sucesso = barbearia.reservar_horario(cliente)
                    if sucesso:
                        print("Horário reservado com sucesso!")
                    else:
                        print("Falha ao reservar horário. Verifique disponibilidade.")

                elif opcao_usuario == 3:
                    clientes = barbearia.listar_clientes()
                    for cliente in clientes:
                        print(f"Nome: {cliente.nome}, CPF: {cliente.cpf}, Corte: {cliente.corte_desejado}, Valor: {cliente.valor}, Dia: {cliente.dia}, Horário: {cliente.horario_desejado}")

                elif opcao_usuario == 4:
                    cpf_cliente = input("CPF do cliente: ")
                    nome = input("Novo nome (deixe vazio para não alterar): ")
                    corte_desejado = input("Novo corte desejado (deixe vazio para não alterar): ")
                    valor = input("Novo valor (deixe vazio para não alterar): ")
                    dia = input("Novo dia (deixe vazio para não alterar): ")
                    horario_desejado = input("Novo horário desejado (deixe vazio para não alterar): ")
                    barbearia.editar_cliente(cpf_cliente, nome=nome, corte_desejado=corte_desejado, valor=float(valor) if valor else None, dia=dia, horario_desejado=horario_desejado)

                elif opcao_usuario == 5:
                    cpf_cliente = input("CPF do cliente: ")
                    barbearia.excluir_cliente(cpf_cliente)
                    print("Cliente excluído com sucesso!")

                elif opcao_usuario == 6:
                    calculadora = CalcularSalarioBarbeiro(barbearia.barbeiro, barbearia.clientes)
                    lucro = calculadora.calcular_lucro()
                    lucro_maior = calculadora.verificar_lucro()
                    print(f"Lucro total: R${lucro:.2f}")
                    if lucro_maior:
                        print("O barbeiro está gerando mais lucro do que o salário dele.")
                    else:
                        print("O barbeiro não está gerando mais lucro do que o salário dele.")

                elif opcao_usuario == 7:
                    break

        elif isinstance(usuario_autenticado, Cliente):
            while True:
                print("1 - Listar horários disponíveis")
                print("2 - Reservar horário")
                print("3 - Sair")
                opcao_usuario = int(input("Escolha uma opção: "))

                if opcao_usuario == 1:
                    dia = menu_dia()
                    if dia != "Opção inválida":
                        horarios = barbearia.listar_horarios_disponiveis(dia)
                        print(f"Horários disponíveis para {dia}: {horarios}")

                elif opcao_usuario == 2:
                    nome_cliente = input("Nome do cliente: ")
                    cpf_cliente = input("CPF do cliente: ")
                    dia = menu_dia()
                    if dia == "Opção inválida":
                        print("Opção de dia inválida.")
                        continue
                    horarios = barbearia.listar_horarios_disponiveis(dia)
                    horario_desejado = menu_horario(horarios)
                    if horario_desejado == "Opção inválida":
                        print("Opção de horário inválida.")
                        continue
                    corte_desejado, valor = menu_corte()
                    if corte_desejado == "Opção inválida":
                        print("Opção de corte inválida.")
                        continue
                    cliente = Cliente(nome_cliente, cpf_cliente, corte_desejado, valor, dia, horario_desejado)
                    sucesso = barbearia.reservar_horario(cliente)
                    if sucesso:
                        print("Horário reservado com sucesso!")
                    else:
                        print("Falha ao reservar horário. Verifique disponibilidade.")

                elif opcao_usuario == 3:
                    break

        elif isinstance(usuario_autenticado, Visitante):
            print("Visitantes não possuem permissões específicas.")
            break

    elif opcao == 5:
        break
