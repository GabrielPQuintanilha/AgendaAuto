print ("---------- TESTE--------------")
agenda_pacientes = open("TotalKids.txt","r")
agenda = dict()
horario = input("Que horas são? Ex: 9h : ")
horario = int(horario)
data=input("Quando é a consulta?")
print("-----------------")
data=str(data)
if 6<=horario<12:
    horario = "Bom dia"
elif 18 > horario >=12:
    horario = "Boa Tarde"
else:
    horario = "Boa Noite"
while True:    
    for paciente in agenda_pacientes:  
        paciente = paciente.strip()
        if paciente.startswith("Unidade"):
            continue
        elif paciente.startswith("Sem descri"):
            continue
        elif paciente.startswith("Ocupado"):
            continue
        else: 
            paciente=paciente.split()
            if paciente [1] == "-":
                if paciente [1] =="anos":
                    continue
                elif paciente [3] =="Livre":
                    continue
                elif paciente [-1] == "ok":
                    paciente_sem_ok = paciente[0:-1]  
                    paciente_sem_ok = paciente_sem_ok[0:-1]
                    print (paciente_sem_ok)
                    sexo = input ("qual Sexo? M/F: ")
                    sexo = sexo.lower().rstrip()
                    if sexo == "m":
                        sexo = "o"
                        sexo_dele = "e"
                    elif sexo == "f":
                        sexo = "a"
                        sexo_dele = "a"
                    print("---")
                    print(horario)  
                    print("Meu nome é Gabriel e eu sou o nutricionista responsável pela consulta d"+sexo, paciente_sem_ok[3],paciente_sem_ok[-1],data, "às",paciente_sem_ok[0], ".")
                    print("Confirmo a presença del"+sexo_dele+"?")
                    print("-----------------")
                    continue
                else:
                    paciente= paciente[0:-1]
                    print(paciente)
                    sexo = input ("qual Sexo? M/F: ")
                    sexo = sexo.lower().rstrip()
                    if sexo == "m":
                        sexo = "o"
                        sexo_dele = "e"
                    elif sexo == "f":
                        sexo = "a"
                        sexo_dele = "a"
                    print("---")
                    print(horario)  
                    print("Meu nome é Gabriel e eu sou o nutricionista responsável pela consulta d"+sexo, paciente[3],paciente[-1],data, "às",paciente[0], ".")
                    print("Confirmo a presença del"+sexo_dele+"?")
                    print("-----------------")
            else:
                if paciente [1] =="anos":
                    continue
                elif paciente [1] =="Livre":
                    continue
                elif paciente [2] =="Paciente":
                    continue
                elif paciente [-1] == "ok":
                    paciente_sem_ok = paciente[0:-1]  
                    paciente_sem_ok = paciente_sem_ok[0:-1]
                    print (paciente_sem_ok)
                    sexo = input ("qual Sexo? M/F: ")
                    sexo = sexo.lower().rstrip()
                    if sexo == "m":
                        sexo = "o"
                        sexo_dele = "e"
                    elif sexo == "f":
                        sexo = "a"
                        sexo_dele = "a"
                    print("---")
                    print(horario)  
                    print("Meu nome é Gabriel e eu sou o nutricionista responsável pela consulta d"+sexo, paciente_sem_ok[1],paciente_sem_ok[-1],data, "às",paciente_sem_ok[0], ".")
                    print("Confirmo a presença del"+sexo_dele+"?")
                    print("-----------------")
                    continue
                else:
                    paciente= paciente[0:-1]
                    print(paciente)
                    sexo = input ("qual Sexo? M/F: ")
                    sexo = sexo.lower().rstrip()
                    if sexo == "m":
                        sexo = "o"
                        sexo_dele = "e"
                    elif sexo == "f":
                        sexo = "a"
                        sexo_dele = "a"
                    print("---")
                    print(horario)  
                    print("Meu nome é Gabriel e eu sou o nutricionista responsável pela consulta d"+sexo, paciente[1],paciente[-1],data, "às",paciente[0], ".")
                    print("Confirmo a presença del"+sexo_dele+"?")
                    print("-----------------")
        


# paciente=input("QUal nome do paciente?")
# paciente_strip=paciente.rstrip()

# horario= input("Que horas?")

# if sexo == "m":
    # sexo = "o"
    # sexo_dele = "e"
# elif sexo == "f":
    # sexo = "a"
    # sexo_dele = "a"
   

# print ("Bom Dia")  
# print("Meu nome é Gabriel e eu sou o nutricionista responsável pela consulta d"+sexo, paciente, "amanhã às",horario, ".")
# print("Confirmo a presença del"+sexo_dele+"?")


