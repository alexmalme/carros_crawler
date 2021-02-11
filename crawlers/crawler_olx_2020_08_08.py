#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 14:40:42 2020

@author: alx_malme
"""

# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import sqlite3
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re
import time
from urllib.parse import unquote
import json


# %%
class Parametros:
    def __init__(self, state, start_url, city, transacao, preco_minimo,
                 preco_maximo, ordem, pagina):
        self.state = state
        self.start_url = start_url
        self.city = city
        self.transacao = transacao
        self.preco_minimo = str(preco_minimo) if str(preco_minimo) != None else ''
        self.preco_maximo = str(preco_maximo) if str(preco_maximo) != None else ''
        self.ordem = ordem
        self.pagina = str(pagina) if str(pagina) not in [None, ''] else '1'
        self.url_compacto = f"https://{self.get_state}.{self.get_start_url}/{self.get_city}-e-regiao/autos-e-pecas" if self.get_city != None else f"https://{self.get_state}.{self.get_start_url}/autos-e-pecas/"
        self.url_default = f"{self.get_url_compacto}/{self.transacao}{self.get_ordem}{self.get_preco_minimo}{self.get_preco_maximo}{self.get_pagina}"
        
    @property
    def get_url_compacto(self):
        return self.url_compacto
    
    @property
    def get_url_default(self):
        return self.url_default
    
    def set_url_default(self, url_compacto=None, transacao=None, ordem=None, preco_minimo=None, preco_maximo=None, pagina=None):
        u_compacto = url_compacto if url_compacto != None else self.get_url_compacto
        t = transacao if transacao != None else self.get_transacao
        o = ordem if ordem != None else self.get_ordem
        p_min = preco_minimo if preco_minimo != None else self.get_preco_minimo
        p_max = preco_maximo if preco_maximo != None else self.get_preco_maximo
        pg = pagina if pagina != None else self.get_pagina
        self.url_default = f"{u_compacto}/{t}{o}{p_min}{p_max}{pg}"

    @property
    def get_state(self):
        return self.state

    @get_state.setter
    def get_state(self, newstate):
        self.state = newstate

    @property
    def get_start_url(self):
        return self.start_url
    
    @get_start_url.setter
    def get_start_url(self, newstart_url):
        self.start_url = newstart_url

    @property
    def get_city(self):
        return self.city
    
    @get_city.setter
    def get_city(self, newcity):
        self.city = newcity

    @property
    def get_transacao(self):
        return self.transacao
    
    @get_transacao.setter
    def get_transacao(self, newtransacao):
        self.transacao = newtransacao + '?'

    @property
    def get_preco_minimo(self):
        return self.preco_minimo
    
    @get_preco_minimo.setter
    def get_preco_minimo(self, newpreco_minimo):
        self.preco_minimo = (f'&ps={newpreco_minimo}')

    @property
    def get_preco_maximo(self):
        return self.preco_maximo
    
    @get_preco_maximo.setter
    def get_preco_maximo(self, newpreco_maximo):
        self.preco_maximo = (f'&pe={newpreco_maximo}')

    @property
    def get_ordem(self):
        return self.ordem
    
    @get_ordem.setter
    def get_ordem(self, newordem):
        """
        Preço: 'sp=1',
        Mais Recentes: 'sf=1',
        Mais Relevantes: ''
        """
        self.ordem = newordem

    @property
    def get_pagina(self):
        return self.pagina
    
    @get_pagina.setter
    def get_pagina(self, newpagina):
        self.pagina = (f'&o={newpagina}')

# %%
    def choose_state(self):
        state = input('Escolha o Estado: \n1: RJ  2: SP ')
        while state.strip() not in ['1', '2']:
            print('Você não escolheu um Estado válido')
            state = input('Escolha o Estado: \n1: RJ  2: SP ')
        if state.strip() == '1':
            state = 'rj'
        elif state.strip() == '2':
            state = 'sp'
        print('Você escolheu:', str(state))
        self.get_state = state

# %%
    def choose_city(self):
        city = input('Escolha a Cidade: \n1: Rio de Janeiro  2: São Paulo ')
        while city.strip() not in ['1', '2']:
            print('Você não escolheu uma city válida')
            city = input('Escolha a Cidade: \n1: Rio de Janeiro  2: São Paulo ')
        if city.strip() == '1':
            city = 'rio-de-janeiro'
        elif city.strip() == '2':
            city = 'sao-paulo'
        print('Você escolheu:', str(city))
        self.get_city = city

# %%
    def choose_ordem(self):
        ordem = input("""Escolha a ordem:
                      f'Preço: 1, Mais Recentes: 2, Mais Relevantes: 3""")
        while ordem.strip() not in ['1', '2', '3']:
            print('Você não escolheu uma ordem válida')
            ordem = input("""Escolha a ordem: 
                          f'Preço: 1, Mais Recentes: 2, Mais Relevantes: 3 """)
        if ordem.strip() == '1':
            ordem = 'sp=1'
        elif ordem.strip() == '2':
            ordem = 'sf=1'
        elif ordem.strip() == '3':
            ordem = ''
        self.get_ordem = ordem

# %%
    def choose_pagina(self):            
        pagina = input("""
        Digite a pagina inicial da pesquisa.
        Use de 1-100\nDefault: 1
        """)
        pagina = ''.join(i for i in pagina if i.isnumeric())
        if pagina in ['', None]:
            pagina = 'o=1'
        self.get_pagina = pagina

# %%
    def choose_preco_minimo(self):
        preco_minimo = input('Digite o preço mínimo. Use apenas números: ')
        if preco_minimo in ['', None]:
            preco_minimo = '0'
        preco_minimo = ''.join(i for i in preco_minimo if i.isnumeric())
        self.get_preco_minimo = preco_minimo

# %%
    def choose_preco_maximo(self):
        preco_maximo = input('''Digite o preço maximo.
        Use apenas números ou aperte enter para não escolher valor limite: ''')
        preco_maximo = ''.join(i for i in preco_maximo if i.isnumeric())
        preco_minimo = ''.join(i for i in self.get_preco_minimo if i.isnumeric())
        while len(preco_maximo) > 1 and int(preco_maximo) < int(preco_minimo):
            preco_maximo = input("""O preço máximo digitado
            é menor que o preço mínimo. Digite o preço maximo. Use apenas números: """)
        if preco_maximo in ['0', None, '']:
            preco_maximo = ''
        preco_maximo = ''.join(i for i in preco_maximo if i.isnumeric())
        self.get_preco_maximo = preco_maximo

# %%
    def escolhe_link(self):
        self.choose_state()
        self.choose_city()
        self.choose_ordem()
        self.choose_pagina()
        self.choose_preco_minimo()
        self.choose_preco_maximo()
        self.set_url_default()

    # %%
    def pergunta_inicial(self):
        link_inicial = input(f'Deseja iniciar a pesquisa no OLX'
                             f'com o link padrão:\n {self.get_url_default} (S/N) ')
        if link_inicial.lower().strip() in ['não', 'n', 'nao']:
            print('Escolha os dados para construção do link inicial')
            self.escolhe_link()

# %%
class Urls(Parametros):

    def __init__(self, state, start_url, city, transacao, preco_minimo,
         preco_maximo, ordem, pagina):
        self.state = state
        self.start_url = start_url
        self.city = city
        self.transacao = transacao
        self.preco_minimo = str(preco_minimo) if str(preco_minimo) != None else ''
        self.preco_maximo = str(preco_maximo) if str(preco_maximo) != None else ''
        self.ordem = ordem
        self.pagina = str(pagina) if str(pagina) not in [None, ''] else 'o=1'
        super().__init__(state, start_url, city, transacao, preco_minimo,
         preco_maximo, ordem, pagina)
        self.url_completo = super().get_url_default

    @property
    def get_url_completo(self):
        return self.url_completo

    def gen_url_completo(self, 
    url_compacto, 
    transacao, 
    ordem, 
    preco_minimo, 
    preco_maximo, 
    pagina):
        self.url_completo = f"{url_compacto}/{transacao}{ordem}{preco_minimo}{preco_maximo}{pagina}"

    def set_url_completo(self, 
    url_compacto='', 
    transacao='carros-vans-e-utilitarios?', 
    ordem='sp=1', 
    preco_minimo='', 
    preco_maximo='', 
    pagina=''
    ):
        u_compacto = url_compacto if url_compacto != '' else self.url_compacto
        t = self.transacao
        o = ordem if ordem != '' else self.ordem
        p_min = preco_minimo if preco_minimo != '' else self.preco_minimo
        p_max = preco_maximo if preco_maximo != '' else self.preco_maximo
        pg = pagina if pagina != '' else self.pagina
        return self.gen_url_completo(u_compacto, t, o, p_min, p_max, pg)
    
    @staticmethod
    def get_time_today():
        time_today = time.strftime("%Y_%m_%d_%H_%M")
        return time_today


    # %%
    def quantos_faltam(self, r):
        rt = r.text.split()
        qts = sorted({int(it.replace('.', '')) for it in rt for t in it if t.isnumeric()})
        return qts


    # %%
    def parse(self, url_completo, url_compacto, count=0):
        print('-'*30)
        print(url_completo)
        print('-'*30, '\n'*2)
        driver = self.driver_()
        driver.get(url_completo)
        items = driver.find_elements_by_xpath('//ul[@id="ad-list"]//a[not(contains(@class, "OLXad-list-link"))]')
        sql, PrecoVenda = None, None
        for item in items:
            if url_compacto in item.get_attribute('href'):
                url_pag = 'view-source:' + item.get_attribute('href')
                print(url_pag)
                # colher os detalhes de cada imóvel
                sql = self.parse_detail(url_pag)
                # salvar no banco de dados
                if sql:
                    self.process_item(sql)
                    PrecoVenda = sql['PrecoVenda']
        try:
            next_page = driver.find_element_by_xpath('//a[@data-lurker-detail="next_page"]').get_attribute('href')
        except:
            next_page = None
            print('-'*30)
            print(f"Última página é {url_completo}")
            print('-'*30)
        if next_page:        
            print('-'*50)
            print(f"Próxima página {next_page}")
            print('-'*50)
            driver.close()
            return self.parse(next_page, url_compacto, count=0)
        else:
            # contagem de quantos imóveis faltam no total
            try:
                r = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[4]/div/div[2]/div[3]/div/span')
            except:
                pass
            try:
                r = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div[2]/div[2]/div/div[8]/div/span')
            except:
                r = None
            finally:
                if r != None:
                    vals = self.quantos_faltam(r)
                    if vals[-1] - vals[-2] <= 50:
                        print("Terminei tudo")
                        driver.close()
                    else:
                    # encontrar o último preço encontrado e colocar ele como preço mínimo
                        if sql:                            
                            ui = self.get_url_completo
                            print(f'Esse é o preço mínimo: {PrecoVenda}')
                            print(f'Esse é o get self.get_preco_minimo{self.get_preco_minimo}')
                            print(f'Esse é o ui: {ui}')
                            #self.set_preco_minimo(PrecoVenda)
                            preco_mininmo = '&ps=' + str(PrecoVenda)
                            self.set_url_completo(preco_minimo=preco_mininmo, pagina='&o=1')
                            print('Olá')
                            print(self.url_completo)
                            driver.close()
                            return self.parse(self.get_url_completo, self.get_url_compacto)
                        else:
                            driver.close()
                            print('Deu erro na hora de pegar quantos faltam para recomeçar')
                else:
                    print('r = None')
                    driver.close()
                    if count >= 3:
                        print('Estou encerrando o programa sem saber para onde ir')
                    else:
                        return self.parse(url_completo, url_compacto, count+1)

    # %%
    def driver_(self):
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        #driver = webdriver.Firefox()
        return driver

    # %%
    def fnan(self, v):
        try:
            val = v
        except:
            val = ''
        return val


    # %%
    def cod_anuncio(self, text):
        rex = re.compile(r'Código do anúncio\: (.*)\.')
        try:
            cods = rex.search(str(text).replace('&lt;br&gt;', '')).group(1)
        except:
            cods = ''
        return cods

    # %%
    def find_num(self, palavra):
        rex = re.compile(r'(\d+)')
        try:
            w = rex.search(str(palavra)).group(1)
        except:
            w = 0
        return int(w)

    
    def parse_detail(self, url):
        try:            
            driver = self.driver_()
            driver.get(url)
            pagina = driver.page_source
            driver.close()
            rex = re.compile(r'window\.dataLayer = (.*}}])')        
            ver = rex.search(pagina).group(1)
            rox= re.compile(r'data-json(.*),.*securityTips')
            tao = rox.search(unquote(pagina)).group(1)
            t = tao.replace('</span>', '').replace('<a class="attribute-value">', '').replace('<span class="entity">','').replace('<span>','').replace('&amp;', '&').replace('&quot;', '"')
            fields = json.loads(t[2:]+'}}')
            dicionario = json.loads(ver[1:-1])
            LinkHref = self.fnan(fields['ad']['friendlyUrl'])
            AnuncioIdPortal = self.fnan(fields['ad']['listId'])
            AnuncioDescricao = self.fnan((fields['ad']['body']).replace('&lt;br&gt;', '. '))
            AnuncioTitulo = self.fnan(fields['ad']['subject'])
            PrecoReais = self.fnan(fields['ad']['priceValue'])
            PrecoVenda = int(self.fnan((str(fields['ad']['priceValue']).replace('R$ ', '')).replace('.','')))
            PrecoAntigo = self.fnan(fields['ad']['oldPrice'])
            TipoAnunciante = 'proprietario' if fields['ad']['professionalAd'] == False else 'profissional'
            AnuncioPortal = 'OLX'
            ContaNome = self.fnan( fields['ad']['user']['name'])
            AnuncianteId = self.fnan(fields['ad']['user']['userId'])
            AnuncioAnuncianteContatoTelefone = self.fnan(fields['ad']['phone']['phone'])
            AnuncioDataCaptura = self.get_time_today()
            Bairro = self.fnan(fields['ad']['location']['neighbourhood'])
            AnuncioEnderecoRua = self.fnan(fields['ad']['location']['address'])
            AnuncioEnderecoCep = self.fnan(fields['ad']['location']['zipcode'])
            AnuncioEnderecoCidade = self.fnan(fields['ad']['location']['municipality'])
            AnuncioEnderecoZona = self.fnan((fields['ad']['location']['zone']).replace('-', ' ').title())    
            AnuncioEnderecoEstado  = 'Rio de Janeiro' if fields['ad']['location']['uf'] == 'RJ' else fields['ad']['location']['uf']    
            AnuncioEnderecoEstadoCod = self.fnan(dicionario['page']['detail']['state_id'])           
            AnuncioCriadoEm = self.fnan((fields['ad']['listTime']).replace('T', ' ').replace('Z', ''))    
            VeiculoModelo = self.fnan([fields['ad']['trackingSpecificData'][i]['value'] for i,val in enumerate(fields['ad']['trackingSpecificData']) if val['key'] == 'model'][0]) if [fields['ad']['trackingSpecificData'][i]['value'] for i,val in enumerate(fields['ad']['trackingSpecificData']) if val['key'] == 'model'] != [] else 0
            VeiculoModeloCompleto = self.fnan([fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['label'] == 'Modelo'][0]) if [fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['label'] == 'Modelo'] != [] else 0
            VeiculoMarca = self.fnan([fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['label'] == 'Marca'][0]) if [fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['label'] == 'Marca'] != [] else 0
            VeiculoTipo = self.fnan([fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'cartype'][0]) if [fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'cartype'] != [] else 0
            VeiculoAno = int(self.fnan([fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['label'] == 'Ano'][0])) if [fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['label'] == 'Ano'] != [] else 0
            VeiculoQuilometragem = self.fnan([fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['label'] == 'Quilometragem'][0]).replace('.','') if [fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['label'] == 'Quilometragem'] != [] else 0
            VeiculoPotencia = self.fnan([fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'motorpower'][0]) if [fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'motorpower'] != [] else 0
            VeiculoCombustivel = self.fnan([fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'fuel'][0]) if [fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'fuel'] != [] else 0
            VeiculoCambio = self.fnan([fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'gearbox'][0]) if [fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'gearbox'] != [] else 0
            VeiculoDirecao = self.fnan([fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'car_steering'][0]) if [fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'car_steering'] != [] else 0
            VeiculoCor = self.find_num([fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'carcolor'][0]) if [fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'carcolor'] != [] else 0       
            VeiculoPortas = self.find_num([fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'doors'][0]) if [fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'doors'] != [] else 0
            VeiculoFinalPlaca = self.find_num([fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'end_tag'][0]) if [fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'end_tag'] != [] else 0
            VeiculoUnicoDono = self.fnan([fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'owner'][0]) if [fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'owner'] != [] else 0
            VeiculoEstadoFinanceiro = str(self.fnan([fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'financial'])) if [fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'financial'] != [] else 0
            VeiculoOpcionais = str(self.fnan([fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'car_features'])) if [fields['ad']['properties'][i]['value'] for i,val in enumerate(fields['ad']['properties']) if val['name'] == 'car_features'] != [] else 0
            item = {"LinkHref": LinkHref,
                    "AnuncioIdPortal": AnuncioIdPortal,
                    "AnuncioDescricao": AnuncioDescricao,
                    "AnuncioTitulo": AnuncioTitulo,
                    "PrecoReais": PrecoReais,
                    "PrecoVenda": PrecoVenda,
                    "PrecoAntigo": PrecoAntigo,
                    "TipoAnunciante": TipoAnunciante,
                    "AnuncioPortal": AnuncioPortal,
                    "ContaNome": ContaNome,
                    "AnuncianteId": AnuncianteId,
                    "AnuncioAnuncianteContatoTelefone": AnuncioAnuncianteContatoTelefone,
                    "AnuncioDataCaptura": AnuncioDataCaptura,
                    "Bairro": Bairro,
                    "AnuncioEnderecoRua": AnuncioEnderecoRua,
                    "AnuncioEnderecoCep": AnuncioEnderecoCep,
                    "AnuncioEnderecoCidade": AnuncioEnderecoCidade,
                    "AnuncioEnderecoZona": AnuncioEnderecoZona,
                    "AnuncioEnderecoEstado": AnuncioEnderecoEstado,
                    "AnuncioEnderecoEstadoCod": AnuncioEnderecoEstadoCod,
                    "AnuncioCriadoEm": AnuncioCriadoEm,
                    "VeiculoModelo": VeiculoModelo,
                    "VeiculoModeloCompleto": VeiculoModeloCompleto,
                    "VeiculoMarca": VeiculoMarca,
                    "VeiculoTipo": VeiculoTipo,
                    "VeiculoAno": VeiculoAno,
                    "VeiculoQuilometragem": VeiculoQuilometragem,
                    "VeiculoPotencia": VeiculoPotencia,
                    "VeiculoCombustivel": VeiculoCombustivel,
                    "VeiculoCambio": VeiculoCambio,
                    "VeiculoDirecao": VeiculoDirecao,
                    "VeiculoCor": VeiculoCor,
                    "VeiculoPortas": VeiculoPortas,
                    "VeiculoFinalPlaca": VeiculoFinalPlaca,
                    "VeiculoUnicoDono": VeiculoUnicoDono,
                    "VeiculoEstadoFinanceiro": VeiculoEstadoFinanceiro,
                    "VeiculoOpcionais": VeiculoOpcionais}
            print(item)
            return item
        except:
            print('Deu Erro')
            return None


    # %%
    def process_item(self, item):    
        conn = sqlite3.connect('/home/alx_malme/carros/db/db_2020_08_28.db')
        conn.execute('''insert into olx(
            LinkHref, 
            AnuncioIdPortal, 
            AnuncioDescricao, 
            AnuncioTitulo, 
            PrecoReais, 
            PrecoVenda, 
            PrecoAntigo, 
            TipoAnunciante, 
            AnuncioPortal, 
            ContaNome, 
            AnuncianteId, 
            AnuncioAnuncianteContatoTelefone, 
            AnuncioDataCaptura, 
            Bairro, 
            AnuncioEnderecoRua, 
            AnuncioEnderecoCep, 
            AnuncioEnderecoCidade, 
            AnuncioEnderecoZona, 
            AnuncioEnderecoEstado, 
            AnuncioEnderecoEstadoCod, 
            AnuncioCriadoEm,
            VeiculoModelo, 
            VeiculoModeloCompleto, 
            VeiculoMarca, 
            VeiculoTipo, 
            VeiculoAno, 
            VeiculoQuilometragem, 
            VeiculoPotencia, 
            VeiculoCombustivel, 
            VeiculoCambio, 
            VeiculoDirecao, 
            VeiculoCor, 
            VeiculoPortas, 
            VeiculoFinalPlaca, 
            VeiculoUnicoDono, 
            VeiculoEstadoFinanceiro, 
            VeiculoOpcionais)
        values (
            :LinkHref, 
            :AnuncioIdPortal, 
            :AnuncioDescricao, 
            :AnuncioTitulo, 
            :PrecoReais, 
            :PrecoVenda, 
            :PrecoAntigo, 
            :TipoAnunciante, 
            :AnuncioPortal, 
            :ContaNome, 
            :AnuncianteId, 
            :AnuncioAnuncianteContatoTelefone, 
            :AnuncioDataCaptura, 
            :Bairro, 
            :AnuncioEnderecoRua, 
            :AnuncioEnderecoCep, 
            :AnuncioEnderecoCidade, 
            :AnuncioEnderecoZona, 
            :AnuncioEnderecoEstado, 
            :AnuncioEnderecoEstadoCod, 
            :AnuncioCriadoEm, 
            :VeiculoModelo, 
            :VeiculoModeloCompleto, 
            :VeiculoMarca, 
            :VeiculoTipo, 
            :VeiculoAno, 
            :VeiculoQuilometragem, 
            :VeiculoPotencia, 
            :VeiculoCombustivel, 
            :VeiculoCambio, 
            :VeiculoDirecao, 
            :VeiculoCor, 
            :VeiculoPortas, 
            :VeiculoFinalPlaca, 
            :VeiculoUnicoDono, 
            :VeiculoEstadoFinanceiro, 
            :VeiculoOpcionais)''',
            item)
        conn.commit()
        conn.close()

    # %%
    def process_item2(self, sql):
        print('Estou no process_item_2')
        print(sql)


# %%
def main():
    parametros = Parametros(
    state='rj',
    start_url='olx.com.br',
    city='rio-de-janeiro',
    transacao='carros-vans-e-utilitarios?',
    preco_minimo='&ps=10000',
    preco_maximo='',
    ordem='sp=1',
    pagina='&o=1'
    )
    parametros.pergunta_inicial()
    #u = Urls(parametros.url_default)
    s, su, c, t, pmin, pmax, o, pg, ud, uc = (parametros.get_state, 
                                              parametros.get_start_url, 
                                              parametros.get_city, 
                                              parametros.get_transacao, 
                                              parametros.get_preco_minimo, 
                                              parametros.get_preco_maximo, 
                                              parametros.get_ordem, 
                                              parametros.get_pagina, 
                                              parametros.get_url_default, 
                                              parametros.get_url_compacto
                                              )
    u = Urls(s, su, c, t, pmin, pmax, o, pg)
    u.parse(ud, uc)


# %%
if __name__ == "__main__":
    main()
    