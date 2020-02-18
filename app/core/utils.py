# import csv
# import pandas as pd
# # from models import Provincia
#
# # def carica_provincie()
# # file_reader = csv.reader('provincia-regione-sigla.csv', delimiter=',')
# # print (file_reader)
# cols = ['provincia', 'regione', 'cod']
# df = pd.read_csv('provincia-regione-sigla.csv',',',
#     encoding = "ISO-8859-1", names=cols)
# # print (df.columns)
# # prov=Provincia
# for r in df.index:
#     print(df.iloc[r]['provincia'])
#     # Provincia.objects.create(
#     # nome=df.iloc[r]['provincia'])
#     # Provincia.save()
# # with open('provincia-regione-sigla.csv', 'rb') as f:
# #     print (f)
# #     r = csv.reader(f)
# #     print (dir(r))
# #     print (r.line_num)
#
#     # for row in r:
#     # # do something with row data.
#     #     print(row)
