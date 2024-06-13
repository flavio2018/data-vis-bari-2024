import streamlit as st
import plotly
import pandas as pd 
import plotly.figure_factory as ff
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns



def add_plesso_to_df(df_voti_liste_comunali_sezioni, sezioni_to_plesso):
	df_voti_liste_comunali_sezioni['PLESSO'] = df_voti_liste_comunali_sezioni.iloc[:-2]['SEZIONE'].apply(lambda sez: sezioni_to_plesso[sez])
	return df_voti_liste_comunali_sezioni


def get_sezioni_to_plesso():
	df_sedi_seggio = pd.read_csv('./data/sedi_seggio.csv')
	sezioni_to_plesso = {}

	for plesso in df_sedi_seggio.iterrows():
	    n_plesso = plesso[1]['numero_plesso']
	    for sezione in eval(plesso[1]['numero_sezione']):
	        sezioni_to_plesso[int(sezione)] = n_plesso

	return sezioni_to_plesso


def plot_hexmap_party(df, party_name):
	fig = ff.create_hexbin_mapbox(
	    data_frame=df, 
	    #labels={"hover_name": 'PLESSO'},
	    lat="lat", lon="lng",
	    nx_hexagon=40, opacity=0.7, 
	    color=party_name,
	    zoom=10.55,
	    center={'lat': 41.1035287, 'lon': 16.8427308},
	    #range_color=[0,0.6],
	    #labels={"color": "Point Count"},
	    width=700,
	)
	fig.update_layout(mapbox_style="carto-positron")
	fig.update_layout(margin=dict(b=0, t=0, l=0, r=0))
	fig.update_layout(coloraxis_colorbar_orientation='h')
	fig.update_layout(coloraxis_colorbar_y=-0.2)

	st.plotly_chart(fig, theme=None)


def reg_plot_parties(df_voti, party1, party2):
	fig, ax = plt.subplots(1, 1, figsize=(7, 6))
	ax = sns.regplot(data=df_voti.iloc[:-1], x=party1, y=party2, ax=ax)
	st.pyplot(fig)


def make_joined_df(df_voti):
	sezioni_to_plesso = get_sezioni_to_plesso()
	df_voti = add_plesso_to_df(df_voti, sezioni_to_plesso)
	df_sedi_seggio_geocoded = pd.read_csv('./data/sedi_seggio_geocoded.csv')
	df_voti_joined = df_voti.join(df_sedi_seggio_geocoded.set_index('numero_plesso'), 'PLESSO')
	return df_voti_joined
    

# px.set_mapbox_access_token(open("../.mapbox_token").read())

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

tab1, tab2 = st.tabs(["Voti sul territorio", "Similarità tra liste"])


with tab1:
	st.title("Elezioni comunali Bari 2024")
	st.header("Dove le liste hanno preso più voti?")
	st.write("Esplora la distribuzione dei voti di singole liste o coalizioni sul territorio. "
			 "Ogni esagono corrisponde a uno più seggi elettorali vicini. "
			 "Il numero assoluto di voti nei seggi può essere normalizzato sul totale nel seggio o sul totale dei voti presi dalla lista.")

	left_column, right_column = st.columns([3, 2])
	normalizza_su = right_column.selectbox('Normalizza su', ['Totale sezione', 'Totale lista'])

	party_name = left_column.selectbox(
	    'Scegli un partito o coalizione',
	     partiti_o_coalizioni)

	if normalizza_su == 'Voti assoluti':
		df_voti = pd.read_csv('./data/voti_liste_coalizioni_sezioni.csv')
	elif normalizza_su == 'Totale sezione':
		df_voti = pd.read_csv('./data/voti_liste_coalizioni_sezioni_norm_sezioni.csv')
	elif normalizza_su == 'Totale lista':
		df_voti = pd.read_csv('./data/voti_liste_coalizioni_sezioni_norm_liste.csv')
	
	df_voti_joined = make_joined_df(df_voti)

	plot_hexmap_party(df_voti_joined, party_name)


with tab2:
	st.title("Elezioni comunali Bari 2024")
	st.header("Quanto è simile l'elettorato delle diverse liste?")
	st.write("Ogni punto nel grafico è un seggio e i valori rappresentano i voti presi da una lista in quel seggio in numero assoluto. "
			 "Il grafico mette a confronto i voti presi da due liste in tutti i seggi della città. "
			 "Prova a confrontare, ad esempio, le liste *Bari Bene Comune* e *Europa Verde - Verdi*.")

	party_1 = st.selectbox(
	    'Scegli la prima lista',
	    partiti_o_coalizioni[:-4],
	    key=1
	)

	party_2 = st.selectbox(
	    'Scegli la seconda lista',
	    partiti_o_coalizioni[:-4],
	    key=2
	)

	df_voti = pd.read_csv('./data/voti_liste_coalizioni_sezioni.csv')
	df_voti_joined = make_joined_df(df_voti)
	
	reg_plot_parties(df_voti, party_1, party_2)
