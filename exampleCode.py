    # Example of adding a row to the sheet
        #     add_row_to_sheet(sheet, {
        #     'Principio Attivo': '1',
        #     'Descrizione Gruppo': '2',
        #     'Denominazione e Confezione': '3',
        #     'Titolare AIC': '4',
        #     'Codice  AIC': '5',
        #     'Codice Gruppo Equivalenza': '6',
        #     'Class': '7',
        #     '4.1 Indicazioni terapeutiche': '8',
        #     '4.2 Posologia e modo di somministrazione': '9',
        #     '4.3 Contraindications': '10',
        #     '4.4 Special warnings and precautions for use': '11',
        #     '4.5 Interactions with other medicinal products': '12',
        #     '4.6 Fertility, pregnancy and lactation': '13',
        #     '4.7 Effects on ability to drive and use machines': '14',
        #     '4.8 Undesirable effects (side effects)': '15',
        #     '4.9 Overdose': 'Overdose example',
        #     '6.2 Incompatibilities': '16',
        #     'CLASS': '17',
        #     'URL': '18',
        #     'URL_json': '19'
        # })
        
        # Example of retrieving all rows from the sheet
        # result = get_all_rows(sheet, column_names=[
        #     'Codice  AIC'
        # ])
        # for item in result:
            # print(item['Codice  AIC'])
        # Example of updating a row in the sheet
        # update_row_in_sheet(sheet, 'Codice  AIC', '5', {
        #     'Principio Attivo': "AAAAAAAAAA", 'Descrizione Gruppo': "A",
        #     'Denominazione e Confezione': "A", 'Titolare AIC': "A",
        #     'Codice  AIC': "5", 'Codice Gruppo Equivalenza': "A",
        #     'Class': "A", '4.1 Indicazioni terapeutiche': "A",
        #     '4.2 Posologia e modo di somministrazione': "A",
        #     '4.3 Contraindications': "A",
        #     '4.4 Special warnings and precautions for use': "A",
        #     '4.5 Interactions with other medicinal products': "A",
        #     '4.6 Fertility, pregnancy and lactation': "A",
        #     '4.7 Effects on ability to drive and use machines': "A",
        #     '4.8 Undesirable effects (side effects)': "A",
        #     '4.9 Overdose': "A",
        #     '6.2 Incompatibilities': "A",
        #     'CLASS': "A",
        #     'ATC': "A",
        #     'URL': "A",
        #     'URL_json': "A"
        # })
        # # Example of getting rows by column value
        # result = get_rows_by_column_value(sheet, 'Codice  AIC', '5')
        # print(result)
