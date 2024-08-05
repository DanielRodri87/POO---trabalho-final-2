import os
import abc
from typing import List, Dict, Optional

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPressione Enter para continuar...")

class Autenticavel(abc.ABC):
    def obter_permissoes(self):
        pass

class Pessoa:
    def __init__(self, nome, cpf):
        self._nome = nome
        self._cpf = cpf

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def cpf(self):
        return self._cpf

class Barbeiro(Pessoa):
    def __init__(self, nome, cpf, salario):
        super().__init__(nome, cpf)
        self._horarios_livres = {
            "Segunda": [],
            "Terça": [],
            "Quarta": [],
            "Quinta": [],
            "Sexta": [],
            "Sábado": []
        }
        self._salario = salario

    @property
    def horarios_livres(self):
        return self._horarios_livres

    @property
    def salario(self):
        return self._salario

    @salario.setter
    def salario(self, salario):
        self._salario = salario

    def adicionar_horario_livre(self, dia, horario):
        if dia in self._horarios_livres:
            self._horarios_livres[dia].append(horario)
        else:
            raise ValueError("Dia inválido.")

    def remover_horario_livre(self, dia, horario):
        if dia in self._horarios_livres and horario in self._horarios_livres[dia]:
            self._horarios_livres[dia].remove(horario)
        else:
            raise ValueError("Horário não encontrado para o dia especificado.")

    def obter_permissoes(self):
        return ["listar_horarios", "reservar_horario", "listar_clientes", "editar_cliente", "excluir_cliente"]

class Cliente(Pessoa):
    def __init__(self, nome, cpf, corte_desejado, valor, dia, horario_desejado):
        super().__init__(nome, cpf)
        self._corte_desejado = corte_desejado
        self._valor = valor
        self._dia = dia
        self._horario_desejado = horario_desejado

    @property
    def corte_desejado(self):
        return self._corte_desejado

    @corte_desejado.setter
    def corte_desejado(self, corte_desejado):
        self._corte_desejado = corte_desejado

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, valor):
        self._valor = valor

    @property
    def dia(self):
        return self._dia

    @dia.setter
    def dia(self, dia):
        self._dia = dia

    @property
    def horario_desejado(self):
        return self._horario_desejado

    @horario_desejado.setter
    def horario_desejado(self, horario_desejado):
        self._horario_desejado = horario_desejado

    def obter_permissoes(self):
        return ["listar_horarios", "reservar_horario"]

class Visitante(Pessoa):
    def __init__(self, nome, cpf):
        super().__init__(nome, cpf)

class Barbearia:
    def __init__(self, barbeiro):
        self._barbeiro = barbeiro
        self._clientes = []

    @property
    def barbeiro(self):
        return self._barbeiro

    @property
    def clientes(self):
        return self._clientes

    def listar_horarios_disponiveis(self, dia):
        if dia in self._barbeiro.horarios_livres:
            return self._barbeiro.horarios_livres[dia]
        else:
            raise ValueError("Dia inválido.")

    def reservar_horario(self, cliente):
        if cliente.dia in self._barbeiro.horarios_livres and cliente.horario_desejado in self._barbeiro.horarios_livres[cliente.dia]:
            self._clientes.append(cliente)
            self._barbeiro.remover_horario_livre(cliente.dia, cliente.horario_desejado)
            return True
        return False

    def listar_clientes(self):
        return self._clientes

    def editar_cliente(self, cpf, **kwargs):
        for cliente in self._clientes:
            if cliente.cpf == cpf:
                cliente.nome = kwargs.get('nome', cliente.nome)
                cliente.corte_desejado = kwargs.get('corte_desejado', cliente.corte_desejado)
                cliente.valor = kwargs.get('valor', cliente.valor)
                cliente.dia = kwargs.get('dia', cliente.dia)
                cliente.horario_desejado = kwargs.get('horario_desejado', cliente.horario_desejado)
                return
        raise ValueError("Cliente não encontrado.")

    def excluir_cliente(self, cpf):
        for cliente in self._clientes:
            if cliente.cpf == cpf:
                dia = cliente.dia
                horario = cliente.horario_desejado
                self._barbeiro.adicionar_horario_livre(dia, horario)
                self._clientes.remove(cliente)
                del cadastrar.usuarios[cpf]
                return
        raise ValueError("Cliente não encontrado.")

class CalcularSalarioBarbeiro:
    def __init__(self, barbeiro, clientes):
        self._barbeiro = barbeiro
        self._clientes = clientes

    def calcular_lucro(self):
        total = sum(cliente.valor for cliente in self._clientes)
        return total

    def verificar_lucro(self):
        return self.calcular_lucro() > self._barbeiro.salario

# Classes de Login e Cadastro
class Login:
    def __init__(self, usuarios):
        self._usuarios = usuarios

    def autenticar(self, cpf):
        return self._usuarios.get(cpf)

class Cadastrar:
    def __init__(self):
        self._usuarios = {}

    @property
    def usuarios(self):
        return self._usuarios

    def cadastrar_barbeiro(self, nome, cpf, salario):
        if cpf in self._usuarios:
            raise ValueError("CPF já cadastrado.")
        barbeiro = Barbeiro(nome, cpf, salario)
        self._usuarios[cpf] = barbeiro

    def cadastrar_cliente(self, nome, cpf, corte_desejado, valor, dia, horario_desejado):
        if cpf in self._usuarios:
            raise ValueError("CPF já cadastrado.")
        cliente = Cliente(nome, cpf, corte_desejado, valor, dia, horario_desejado)
        self._usuarios[cpf] = cliente

    def cadastrar_visitante(self, nome, cpf):
        if cpf in self._usuarios:
            raise ValueError("CPF já cadastrado.")
        visitante = Visitante(nome, cpf)
        self._usuarios[cpf] = visitante

    def existe_barbeiro_cadastrado(self):
        return any(isinstance(usuario, Barbeiro) for usuario in self._usuarios.values())

class Menu:
    @staticmethod
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

    @staticmethod
    def menu_corte():
        clear_screen()
        print("=" * 30)
        print("   | ESCOLHA CORTE |")
        print("=" * 30)
        print("\nEscolha o tipo de corte:\n")
        print("1 - Americano  | R$ 15,00")
        print("2 - Mullet     | R$ 15,00")
        print("3 - Low Fade   | R$ 18,00")
        print("4 - Social     | R$ 12,00")
        print("=" * 30)
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

    @staticmethod
    def menu_dia():
        clear_screen()
        print("=" * 30)
        print("   📅 Escolha o Dia da Semana")
        print("=" * 30)
        print("\n1 - Segunda  | 🌞")
        print("2 - Terça    | 🌞")
        print("3 - Quarta   | 🌞")
        print("4 - Quinta   | 🌞")
        print("5 - Sexta    | 🌞")
        print("6 - Sábado   | 🌟")
        print("=" * 30)
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

    @staticmethod
    def menu_hora(dia, barbeiro):
        clear_screen()
        horarios = barbeiro.horarios_livres.get(dia, [])
        print(f"\nHorários disponíveis para {dia}: {', '.join(horarios)}")
        horario = input("Escolha um horário: ")
        if horario in horarios:
            return horario
        return "Horário inválido"

    @staticmethod
    def menu_principal():
        clear_screen()
        print("=" * 30)
        print("  💈 Sistema de Agendamento de Barbearia 💈")
        print("=" * 30)
        print("\n1️⃣  - Login")
        print("2️⃣  - Cadastrar")
        print("0️⃣  - Sair")
        print("=" * 30)
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return -1

    @staticmethod
    def menu_login():
        clear_screen()
        cpf = input("Digite seu CPF: ")
        return cpf

    @staticmethod
    def menu_cadastrar():
        print("=" * 30)
        print("   🙍‍♂️ Escolha o Tipo de Usuário 🙍‍♀️")
        print("=" * 30)
        print("\n1️⃣  - Barbeiro ✂️")
        print("2️⃣  - Cliente 👤")
        print("3️⃣  - Visitante 👀")
        print("=" * 30)
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            return -1

    @staticmethod
    def menu_horario(horarios):
        clear_screen()
        print("\nEscolha o horário:")
        for idx, horario in enumerate(horarios, 1):
            print(f"{idx} - {horario}")
        try:
            opcao = int(input("Escolha uma opção: "))
            if 1 <= opcao <= len(horarios):
                return horarios[opcao - 1]
            return "Opção inválida"
        except ValueError:
            return "Opção inválida"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPressione Enter para continuar...")



Autenticavel.register(Barbeiro)
Autenticavel.register(Cliente)

visitante = Visitante("impostor", "111")
# login = Login({"111": visitante})
menu = Menu()
cadastrar = Cadastrar()
login = Login(cadastrar.usuarios)
barbearia = None

while True:
    clear_screen()
    print("=" * 45)
    print("          💈 MENU PRINCIPAL 💈          ")
    print("=" * 45)
    print("\n1️⃣  - Cadastrar Barbeiro ✂️")
    print("2️⃣  - Cadastrar Cliente 👤")
    print("3️⃣  - Fazer Login 🔑")
    print("4️⃣  - Sair 🚪")
    print("=" * 45)
    opcao = input("\nEscolha uma opção: ")

    if opcao == '1':
        clear_screen()
        print("\n===== ✂️ CADASTRAR BARBEIRO ✂️ =====\n")
        
        if cadastrar.existe_barbeiro_cadastrado():
            print("Já existe um barbeiro cadastrado.")
            pause()
            continue
        
        nome = input("Nome: ")
        cpf = input("CPF: ")
        try:
            salario = float(input("Salário: "))
        except ValueError:
            print("Entrada inválida para salário. Por favor, insira um número.")
            pause()
            continue
        cadastrar.cadastrar_barbeiro(nome, cpf, salario)
        barbeiro = cadastrar.usuarios[cpf]  # Captura a referência do barbeiro
        barbearia = Barbearia(barbeiro)
        menu.adicionar_horarios_barbeiro(barbeiro)
        print(f"Barbeiro {nome} cadastrado com sucesso!")
        pause()

    elif opcao == '2':
        clear_screen()
        print("\n===== 👤 CADASTRAR CLIENTE 👤 =====\n")
        if not cadastrar.existe_barbeiro_cadastrado():
            print("Por favor, cadastre um barbeiro antes de cadastrar um cliente.")
            pause()
            continue
        nome = input("Nome: ")
        cpf = input("CPF: ")
        corte_desejado, valor = menu.menu_corte()
        if valor == 0:
            print("Opção inválida de corte.")
            pause()
            continue
        dia = menu.menu_dia()
        if dia == "Opção inválida":
            print("Opção inválida de dia.")
            pause()
            continue
        horarios_disponiveis = barbearia.listar_horarios_disponiveis(dia)
        if not horarios_disponiveis:
            print("Não há horários disponíveis para o dia escolhido.")
            pause()
            continue
        horario_desejado = menu.menu_horario(horarios_disponiveis)
        if horario_desejado == "Opção inválida":
            print("Opção inválida de horário.")
            pause()
            continue
        try:
            cadastrar.cadastrar_cliente(nome, cpf, corte_desejado, valor, dia, horario_desejado)
            cliente = cadastrar.usuarios[cpf]
            if barbearia.reservar_horario(cliente):
                print(f"Cliente {nome} cadastrado e horário reservado com sucesso!")
            else:
                print(f"Falha ao reservar o horário para o cliente {nome}.")
            pause()
        except ValueError as e:
            print(e)
            pause()

    elif opcao == '3':
        clear_screen()
        print("\n===== 🔑 LOGIN 🔑 =====\n")
        cpf = input("CPF: ")
        usuario = login.autenticar(cpf)
        if not usuario:
            print("CPF não encontrado.")
            pause()
            continue
        
        if isinstance(usuario, Autenticavel) == False:
            print("Usuário não tem permissão.")
            pause()
            continue
        
        permissoes = usuario.obter_permissoes()
        if isinstance(usuario, Barbeiro):
            if isinstance(usuario, Autenticavel):
                while True:
                    clear_screen()
                    print(f"\nBem-vindo, Barbeiro {usuario.nome}! ✂️\n")
                    print("1️⃣  - Listar Horários Disponíveis")
                    print("2️⃣  - Reservar Horário")
                    print("3️⃣  - Listar Clientes")
                    print("4️⃣  - Editar Cliente")
                    print("5️⃣  - Excluir Cliente")
                    print("6️⃣  - Calcular Lucro")
                    print("7️⃣  - Sair")
                    opcao_barbeiro = input("\nEscolha uma opção: ")

                    if opcao_barbeiro == '1' and "listar_horarios" in permissoes:
                        dia = menu.menu_dia()
                        if dia == "Opção inválida":
                            print("Opção inválida de dia.")
                            pause()
                            continue
                        horarios_disponiveis = barbearia.listar_horarios_disponiveis(dia)
                        if horarios_disponiveis:
                            print(f"Horários disponíveis para {dia}: {', '.join(horarios_disponiveis)}")
                        else:
                            print("Não há horários disponíveis para o dia escolhido.")
                        pause()

                    elif opcao_barbeiro == '2' and "reservar_horario" in permissoes:
                        print("Esta funcionalidade está disponível apenas para clientes.")
                        pause()

                    elif opcao_barbeiro == '3' and "listar_clientes" in permissoes:
                        clientes = barbearia.listar_clientes()
                        if clientes:
                            for cliente in clientes:
                                print(f"Nome: {cliente.nome}, CPF: {cliente.cpf}, Corte: {cliente.corte_desejado}, Dia: {cliente.dia}, Horário: {cliente.horario_desejado}, Valor: {cliente.valor}")
                        else:
                            print("Nenhum cliente cadastrado.")
                        pause()

                    elif opcao_barbeiro == '4' and "editar_cliente" in permissoes:
                        cpf_cliente = input("CPF do cliente a ser editado: ")
                        clientes = [cliente for cliente in barbearia.clientes if cliente.cpf == cpf_cliente]

                        if not clientes:
                            print("Cliente não encontrado.")
                            pause()
                            continue

                        if len(clientes) > 1:
                            print("Cliente possui mais de um agendamento:")
                            for idx, cliente in enumerate(clientes, 1):
                                print(f"{idx} - Corte: {cliente.corte_desejado}, Dia: {cliente.dia}, Horário: {cliente.horario_desejado}")
                            try:
                                opcao_cliente = int(input("Escolha o número do agendamento a ser editado: "))
                                if 1 <= opcao_cliente <= len(clientes):
                                    cliente_a_editar = clientes[opcao_cliente - 1]
                                else:
                                    print("Opção inválida.")
                                    pause()
                                    continue
                            except ValueError:
                                print("Entrada inválida.")
                                pause()
                                continue
                        else:
                            cliente_a_editar = clientes[0]

                        antigo_dia = cliente_a_editar.dia
                        antigo_horario = cliente_a_editar.horario_desejado

                        while True:
                            clear_screen()
                            print("===== ✂️ EDITAR CLIENTE ✂️ =====")
                            print("1️⃣  - Nome")
                            print("2️⃣  - Corte Desejado")
                            print("3️⃣  - Dia e Horário")
                            print("4️⃣  - Cancelar")
                            opcao_edicao = input("Escolha o que deseja editar: ")

                            if opcao_edicao == '1':
                                novo_nome = input("Novo nome (deixe em branco para não alterar): ")
                                cliente_a_editar.nome = novo_nome or cliente_a_editar.nome
                                print("Nome atualizado com sucesso.")
                                pause()
                                break

                            elif opcao_edicao == '2':
                                novo_corte, novo_valor = menu.menu_corte()
                                if novo_valor == 0:
                                    print("Opção inválida de corte.")
                                    pause()
                                    continue
                                cliente_a_editar.corte_desejado = novo_corte
                                cliente_a_editar.valor = novo_valor
                                print("Corte atualizado com sucesso.")
                                pause()
                                break

                            elif opcao_edicao == '3':
                                novo_dia = menu.menu_dia()
                                if novo_dia == "Opção inválida":
                                    print("Opção inválida de dia.")
                                    pause()
                                    continue
                                barbearia.barbeiro.adicionar_horario_livre(antigo_dia, antigo_horario)  # Adiciona o antigo horário de volta
                                horarios_disponiveis = barbearia.listar_horarios_disponiveis(novo_dia)
                                if not horarios_disponiveis:
                                    print("Não há horários disponíveis para o dia escolhido.")
                                    barbearia.barbeiro.remover_horario_livre(antigo_dia, antigo_horario)  # Remove o horário antigo novamente
                                    pause()
                                    continue
                                novo_horario = menu.menu_horario(horarios_disponiveis)
                                if novo_horario == "Opção inválida":
                                    print("Opção inválida de horário.")
                                    barbearia.barbeiro.remover_horario_livre(antigo_dia, antigo_horario)  # Remove o horário antigo novamente
                                    pause()
                                    continue
                                cliente_a_editar.dia = novo_dia
                                cliente_a_editar.horario_desejado = novo_horario
                                barbearia.barbeiro.remover_horario_livre(novo_dia, novo_horario)  # Remove o novo horário dos disponíveis
                                print("Dia e horário atualizados com sucesso.")
                                pause()
                                break

                            elif opcao_edicao == '4':
                                print("Edição cancelada.")
                                pause()
                                break

                            else:
                                print("Opção inválida.")
                                pause()
                    
                    elif opcao_barbeiro == '5' and "excluir_cliente" in permissoes:
                        cpf_cliente = input("CPF do cliente a ser excluído: ")
                        try:
                            barbearia.excluir_cliente(cpf_cliente)
                            print("Cliente excluído com sucesso.")
                        except ValueError as e:
                            print(e)
                        pause()
                        
                    elif opcao_barbeiro == '6':
                        lucro = CalcularSalarioBarbeiro(barbearia.barbeiro, barbearia.clientes)
                        print(f"Lucro total: {lucro.calcular_lucro()} reais")
                        if lucro.verificar_lucro():
                            print("Parabéns! Você atingiu o salário desejado.")
                        else:
                            print("Você ainda não atingiu o salário desejado.")
                        pause()
                        
                    elif opcao_barbeiro == '7':
                        break
            else: 
                print("Usuário não tem permissão.")
                pause()


        elif isinstance(usuario, Cliente):
            if isinstance(usuario, Autenticavel):
                while True:
                    clear_screen()
                    print("1️⃣  - Listar Horários Disponíveis")
                    print("2️⃣  - Reservar Horário")
                    print("3️⃣  - Sair")
                    opcao_cliente = input("\nEscolha uma opção: ")

                    if opcao_cliente == '1' and "listar_horarios" in permissoes:
                        dia = menu.menu_dia()
                        if dia == "Opção inválida":
                            print("Opção inválida de dia.")
                            pause()
                            continue
                        horarios_disponiveis = barbearia.listar_horarios_disponiveis(dia)
                        if horarios_disponiveis:
                            print(f"Horários disponíveis para {dia}: {', '.join(horarios_disponiveis)}")
                        else:
                            print("Não há horários disponíveis para o dia escolhido.")
                        pause()

                    elif opcao_cliente == '2' and "reservar_horario" in permissoes:
                        dia = menu.menu_dia()
                        if dia == "Opção inválida":
                            print("Opção inválida de dia.")
                            pause()
                            continue
                        horarios_disponiveis = barbearia.listar_horarios_disponiveis(dia)
                        if not horarios_disponiveis:
                            print("Não há horários disponíveis para o dia escolhido.")
                            pause()
                            continue
                        horario_desejado = menu.menu_horario(horarios_disponiveis)
                        if horario_desejado == "Opção inválida":
                            print("Opção inválida de horário.")
                            pause()
                            continue
                        cliente = Cliente(usuario.nome, usuario.cpf, usuario.corte_desejado, usuario.valor, dia, horario_desejado)
                        if barbearia.reservar_horario(cliente):
                            print("Horário reservado com sucesso.")
                        else:
                            print("Falha ao reservar o horário.")
                        pause()

                    elif opcao_cliente == '3':
                        break

                    else:
                        print("Opção inválida.")
                        pause()
            else:
                print("Usuário não tem permissão.")

    elif opcao == '4':
        print("Saindo... Até a próxima! 👋")

        break

    else:
        print("Opção inválida.")
        pause()