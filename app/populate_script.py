import os
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE','app.settings')

import django
django.setup()

from core.models import Provincia

# def add_provincia():
#     p = models.Provincia.get_or_create(nome=)
#     p.save()
    # return p

def populate():

    cols = ['provincia', 'regione', 'cod']
    df = pd.read_csv('provincia-regione-sigla.csv',',',
        encoding = "ISO-8859-1", names=cols)

    for r in df.index:
        print(df.iloc[r]['provincia'])
        p = Provincia.objects.get_or_create(nome=df.iloc[r]['provincia'])
        # p.save()
        # Provincia.objects.create(
        # nome=df.iloc[r]['provincia'])
        # Provincia.save()
    #
    #
    # for enntry in range(N):
    #     top = add_topic

if __name__ =='__main__':
    print ("populate province")
    populate()
    print ("populate complete")
