def correctif(questionnaire):
        for i in questionnaire:
            list_of_reponse= ""
            for y in i[1]:
                if True in y:
                    list_of_reponse += f"{y[0]} ,\n"
            print("La/les réponse/s à la question", f"'{i[0]}'",f"était/ent :\n {list_of_reponse}\n")
   
        
