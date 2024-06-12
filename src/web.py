import streamlit as st
import plotly
import pandas as pd 
import plotly.figure_factory as ff
import plotly.express as px



def add_plesso_to_df(df_voti_liste_comunali_sezioni, sezioni_to_plesso):
	df_voti_liste_comunali_sezioni['PLESSO'] = df_voti_liste_comunali_sezioni['SEZIONE'].apply(lambda sez: sezioni_to_plesso[sez])
	return df_voti_liste_comunali_sezioni


def get_sezioni_to_plesso(df_sedi_seggio):
	sezioni_to_plesso = {}

	for plesso in df_sedi_seggio.iterrows():
	    n_plesso = plesso[1]['numero_plesso']
	    for sezione in eval(plesso[1]['numero_sezione']):
	        sezioni_to_plesso[int(sezione)] = n_plesso

	return sezioni_to_plesso


def plot_hexmap_party(df, party_name):
	fig = ff.create_hexbin_mapbox(
	    data_frame=filtered_df_voti, 
	    #labels={"hover_name": 'PLESSO'},
	    lat="lat", lon="lng",
	    nx_hexagon=40, opacity=0.7, 
	    color=party_name,
	    zoom=10.7,
	    #range_color=[0,0.6],
	    #labels={"color": "Point Count"},
	    width=700,
	)
	fig.update_layout(mapbox_style="carto-positron")
	fig.update_layout(margin=dict(b=0, t=0, l=0, r=0))

	st.plotly_chart(fig, theme=None)


px.set_mapbox_access_token(open("../.mapbox_token").read())

df_sedi_seggio = pd.read_csv('../data/sedi_seggio.csv')
df_sedi_seggio_geocoded = pd.read_csv('../data/sedi_seggio_geocoded.csv')
df_voti_liste_comunali_sezioni = pd.read_csv('../data/voti_liste_coalizioni_sezioni_perc.csv')

sezioni_to_plesso = get_sezioni_to_plesso(df_sedi_seggio)
df_voti_liste_comunali_sezioni = add_plesso_to_df(df_voti_liste_comunali_sezioni, sezioni_to_plesso)

df_voti_joined = df_voti_liste_comunali_sezioni.join(df_sedi_seggio_geocoded.set_index('numero_plesso'), 'PLESSO')

filtered_df_voti = df_voti_joined[df_voti_joined['formatted_address'].str.count('Bari BA, Italy') > 0]

partiti_o_coalizioni = ['SCIACOVELLI SINDACO - CI PIACE!',
       'NOI PER BARI - ITALEXIT PER L\'ITALIA PER SCIACOVELLI SINDACO',
       'BARI CITTÀ D\'EUROPA', 'MOVIMENTO CINQUE STELLE', 'GENERAZIONE URBANA',
       'BARI BENE COMUNE', 'PCI - PARTITO COMUNISTA ITALIANO',
       'LAFORGIA SINDACO', 'NOI POPOLARI', 'PROGETTO BARI CON LECCESE',
       'PARTITO DEMOCRATICO', 'LECCESE SINDACO', 'CON LECCESE SINDACO',
       'DECARO PER BARI', 'EUROPA VERDE - VERDI', 'BARI X FABIO ROMITO',
       'AGORÀ', 'MARIO CONCA PER BARI',
       'NOI MODERATI - RIPRENDIAMOCI IL FUTURO',
       'LIBERALI E RIFORMISTI - nPSI',
       'UDC - PRIMA L\'ITALIA PER ROMITO SINDACO', 'FRATELLI D\'ITALIA',
       'FORZA ITALIA', 'ROMITO SINDACO', 'PENSIONATI E INVALIDI',
       'OLTRE MANGANO SINDACO', 'COALIZIONE ROMITO', 'COALIZIONE LECCESE', 'COALIZIONE LAFORGIA']

st.title("Elezioni comunali Bari 2024")
st.write("Esplora la distribuzione dei voti di singoli partiti o coalizioni sul territorio. "
		 "Ogni esagono corrisponde a un seggio elettorale. I valori sono percentuali sul totale dei voti nel seggio.")

party_name = st.selectbox(
    'Scegli un partito o coalizione',
     partiti_o_coalizioni)

plot_hexmap_party(filtered_df_voti, party_name)