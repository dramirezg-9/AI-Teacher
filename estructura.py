# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 12:03:43 2020

@author: Netie
"""


from sympy import *

def libre1(expresion:str)-> list:
    from parsing import parsing
    
    libres = []
    primaria = parsing(expresion)[-1]
    operaciones = [["+","-"],["*","/"]]

    central = operaciones[0]
    operador = primaria
    if primaria in operaciones[1]:
        operador = "*"
        central = operaciones[1]
    
    i = 0
    print(central)
    
    while i<len(expresion):
        pase = False
        primero = ""
        
        while i<len(expresion) and ((expresion[i] not in central) or pase):
            print(primero,pase)
            print((expresion[i] not in central))
            if expresion[i] == "(":
                pase = True
            elif expresion[i] == ")":
                pase = False
            primero += expresion[i]
            i+=1
            
  
        libres.append((operador,primero))
        if i<len(expresion):
            operador = expresion[i]
        i +=1
        
    return libres

def evaluar_numerica(ecuacuacion:str,variables:dict)->int:
    
    for variable in variables:
        ecuacuacion = ecuacuacion.replace(variable, str(variables[variable]))
    resultado = eval(ecuacuacion)
    return resultado


def separar_igualdad(ecuacion:str)->list:
    partes = [-2]
    comp = []
    ecuacion =   ecuacion
    for i in range(len(ecuacion)):
        if ecuacion[i] in "=<>":
             partes.append(i-1)
    partes.append(len(ecuacion)-1)
    for j in range(len(partes)-1):
        print(partes[j])
        print(partes[j+1])
        comp.append(ecuacion[partes[j]+2:partes[j+1]+1])
    return comp



    

    
    
    