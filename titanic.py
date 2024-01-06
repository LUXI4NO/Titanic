import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

# Configuración de la página de la aplicación
st.set_page_config(page_title="Análisis Titanic", page_icon="🚢", layout="wide")
df = pd.read_csv('Tripulantes.CSV', encoding='utf-8')


with st.container():
    text_column,image_column = st.columns((3,2))
    with image_column:
        image = Image.open("Image/tianic3.png")
        st.image(image, width=600)
    with text_column:
        st.write("##")
        st.write("##")
        st.write("##")
        st.title("¡Bienvenido a la Exploración del Trágico Viaje del Titanic!")
        st.write("Descubre las historias detrás de cada persona a bordo del RMS Titanic, el coloso de los mares que protagonizó una de las tragedias más impactantes en la historia marítima. En este análisis de datos, te invitamos a explorar el viaje inaugural del Titanic, que tuvo lugar del 14 al 15 de abril de 1912, desde Southampton a Nueva York, y conocer detalles fascinantes sobre los pasajeros a través de un conjunto de datos detallado.")
        st.write("Este proyecto te ofrece una visión única para comprender la vida a bordo del Titanic, destacando aspectos como la distribución por género, clases sociales, relaciones familiares, y factores que influyeron en la supervivencia de los pasajeros. Sumérgete en la historia y descubre patrones, tendencias y detalles conmovedores que nos conectan con aquel trágico suceso.")
        st.write("¡Explora y analiza los datos del Titanic con nosotros para revivir virtualmente parte de su historia!")

st.write("##")
st.write("##")
st.write("##")
with st.container():
    st.markdown("<h1 style='text-align: center;'>Supervivencia de Pasajeros</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Desde estadísticas generales hasta gráficos interactivos, cada elemento ofrece una visión detallada de aspectos clave, como la distribución de la edad y la relación entre el género y la supervivencia. La presentación clara y concisa permite una comprensión rápida y profunda de los patrones presentes en el conjunto de datos de supervivencia.</p>", unsafe_allow_html=True)

    # Cálculos y tabla de resultados
    total_pasajeros = len(df)
    total_sobrevivientes = df[df['Survived'] == 1].shape[0]
    total_muertos = df[df['Survived'] == 0].shape[0]

    porcentaje_sobrevivientes = round((total_sobrevivientes / total_pasajeros) * 100, 2)
    porcentaje_muertos = round((total_muertos / total_pasajeros) * 100, 2)

    edad_promedio_sobrevivientes = round(df.loc[df['Survived'] == 1, 'Age'].mean(), 2)
    edad_promedio_fallecidos = round(df.loc[df['Survived'] == 0, 'Age'].mean(), 2)
    desviacion_estandar_sobrevivientes = round(df.loc[df['Survived'] == 1, 'Age'].std(), 2)
    desviacion_estandar_fallecidos = round(df.loc[df['Survived'] == 0, 'Age'].std(), 2)

    # Tabla de resultados
    tabla_resultados = pd.DataFrame({
        "Categoría": ["Sobrevivientes",'Fallecidos'],
        "Total": [total_sobrevivientes, total_muertos],
        "Porsentaje": [porcentaje_sobrevivientes, porcentaje_muertos],
        "Promedio Edad": [edad_promedio_sobrevivientes, edad_promedio_fallecidos],
        "Desviacion": [desviacion_estandar_sobrevivientes, desviacion_estandar_fallecidos]
    })

    # Mostrar tabla de resultados sin índice
    st.table(tabla_resultados.set_index('Categoría', drop=True).style 
        .set_properties(**{'text-align': 'center', 'font-size': '18px'})
        .bar(subset=['Total', 'Porsentaje', 'Promedio Edad', 'Desviacion'], color='#83B7E2')
        .highlight_max(axis=0, color='#ECF3FD')
        .format({'Total': '{:.0f}', 'Porsentaje': '{:.0f}%', 'Promedio Edad': '{:.0f}%', 'Desviacion': '{:.0f}'})
        .set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#ECF3FD'), ('color', '#000000'),
                                              ('font-size', '18px'), ('border', '1px solid #000000')]},
                {'selector': 'td', 'props': [('border', '1px solid #000000'), ('color', 'black')]},  # Añadido color negro
                {'selector': 'tr:hover', 'props': [('background-color', '#000000')]},
                {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#EDF3FD')]},
                {'selector': 'tr:nth-child(odd)', 'props': [('background-color', '#EDF3FD')]},
                {'selector': 'td:hover', 'props': [('background-color', '#3580E9'), ('color', 'White')]}
             ])
)

    with st.container():
        # Filtro interactivo para la edad
        edad_filtro = st.slider("Seleccionar Rango de Edad", int(df['Age'].min()), int(df['Age'].max()), (int(df['Age'].min()), int(df['Age'].max())))

        # Aplicar filtro
        df_filtrado = df[(df['Age'] >= edad_filtro[0]) & (df['Age'] <= edad_filtro[1])]

        # Configurar el contenedor principal
        # Configurar columnas
        columna_edad, columna_sobrevivientes = st.columns((3, 2))

        with columna_edad:
            interval = alt.selection_single(encodings=['color'])
            # Ajustar el gráfico de Altair para la edad y la supervivencia
            grafico_edad_sobrevivencia = (
                alt.Chart(df_filtrado).mark_bar().encode(
                    alt.X("Age:Q", bin=True, title="Rango de Edad"),
                    alt.Y("count():Q", title="Cantidad de Pasajeros", axis=alt.Axis(grid=False)),
                    alt.Color("Survived:N", title="Sobrevivientes", scale=alt.Scale(domain=[0, 1], range=['#25549C','#83B7E2']))
                )
                .properties(width=700,height=400,title='Gráfico de Barras - Rango de edad y Supervivencia')
                .add_selection(interval)
                .transform_filter(interval)

            )

            # Mostrar el gráfico en Streamlit
            st.altair_chart(grafico_edad_sobrevivencia, use_container_width=True)

        with columna_sobrevivientes:
            interval = alt.selection_single(encodings=['color'])
            # Ajustar el gráfico de Altair para el género y la supervivencia
            grafico_genero_sobrevivencia = (
                alt.Chart(df_filtrado).mark_bar().encode(
                    alt.X("count()", title="Cantidad de Pasajeros", sort=alt.SortOrder('descending')),
                    alt.Y("Survived:N", title="Supervivencia"),
                    color=alt.Color("Sex:N", title="Género", scale=alt.Scale(domain=['female', 'male'], range=['#25549C','#83B7E2'])),
                    tooltip=[alt.Tooltip('count()', title='Cantidad de Pasajeros'), alt.Tooltip('Survived:N',  title='Sobrevivientes'), alt.Tooltip('Sex:N', title='Sexo')]
                )
                .properties(width=700,height=400,title='Gráfico de Barras - Cantidad de pasajeros y Supervivencia')
                .configure_axis(grid=False)
                .configure_legend(orient='left')
                .configure_axisY(orient='right')
                .add_selection(interval)
                .transform_filter(interval)
            )
            # Mostrar el gráfico en Streamlit
            st.altair_chart(grafico_genero_sobrevivencia, use_container_width=True)


st.write("##")
st.write("##")
# Contenedor para organizar el diseño
with st.container():
    st.markdown("<h1 style='text-align: center;'>Relación entre Clase Socioeconómica y Supervivencia en el Titanic</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Mostrare la relación entre la clase socioeconómica, las tasas de supervivencia de los pasajeros del Titanic. Proporciona visualizaciones intuitivas y filtros interactivos para explorar patrones significativos y obtener una visión profunda de la demografía a bordo del famoso barco. Los gráficos de barras presentados muestran de manera clara y atractiva cómo estos factores se entrelazan, permitiendo a los usuarios explorar y entender mejor los datos históricos del Titanic.</p>", unsafe_allow_html=True)


    # Cálculos previos
    total_pasajeros = len(df)
    total_por_clase = df.groupby('Pclass').size()
    supervivientes_por_clase = df[df['Survived'] == 1].groupby('Pclass').size()
    Fallecidos_por_clase = df[df['Survived'] == 0].groupby('Pclass').size()

    # Cálculo de porcentajes
    porcentaje_supervivientes = (supervivientes_por_clase / total_por_clase * 100)
    porcentaje_fallecidos = (Fallecidos_por_clase / total_por_clase * 100)

    # Creación de un DataFrame con los resultados
    tabla_resultados = pd.DataFrame({
        "Categoría": ["Primera Clase", "Segunda Clase", "Tercera Clase"],
        "Total": total_por_clase.values,
        "Supervivientes": supervivientes_por_clase.values,
        "Fallecidos": Fallecidos_por_clase.values,
        "Porcentaje Supervivientes": porcentaje_supervivientes,
        "Porcentaje Fallecidos": porcentaje_fallecidos,
    })

    # Visualización de resultados en forma de tabla
    st.table(tabla_resultados.set_index('Categoría', drop=True).style 
        .set_properties(**{'text-align': 'center', 'font-size': '18px'})
        .bar(subset=['Total', 'Supervivientes', 'Fallecidos', 'Porcentaje Supervivientes','Porcentaje Fallecidos'], color='#83B7E2')
        .highlight_max(axis=0, color='#ECF3FD')
        .format({'Total': '{:.0f}', 'Supervivientes': '{:.0f}', 'Fallecidos': '{:.0f}', 'Porcentaje Supervivientes': '{:.0f}%', 'Porcentaje Fallecidos': '{:.0f}%'})
        .set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#ECF3FD'), ('color', '#000000'),
                                              ('font-size', '15px'), ('border', '1px solid #000000')]},
                {'selector': 'td', 'props': [('border', '1px solid #000000'), ('color', 'black')]},  # Añadido color negro
                {'selector': 'tr:hover', 'props': [('background-color', '#000000')]},
                {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#EDF3FD')]},
                {'selector': 'tr:nth-child(odd)', 'props': [('background-color', '#EDF3FD')]},
                {'selector': 'td:hover', 'props': [('background-color', '#3580E9'), ('color', 'White')]}
             ]))

    with st.container():
        selected_class = st.multiselect("Seleccionar Clase", sorted(df['Pclass'].unique()))

        
        # Filtrado interactivo por clase
        if selected_class:
            df_filtered = df[df['Pclass'].isin(selected_class)]
        else:
            df_filtered = df

        #Columnas de Los Graficos
        columna_derecha, columna_izquierda = st.columns((2, 2))
        # Gráfico de barras - Clases y Supervivencia
        with columna_izquierda:
            interval = alt.selection_single(encodings=['color'])
            chart_clase_supervivencia = (
                alt.Chart(df_filtered).mark_bar().encode(
                    alt.Y('Pclass:N', title='Clases', axis=alt.Axis(labelAngle=0)),
                    alt.X('count():Q', title='Cantidad de pasajeros', sort=alt.SortOrder('descending')),
                    color=alt.Color("Survived:N", title="Survived", scale=alt.Scale(domain=[0, 1], range=['#83B7E2','#25549C'])),
                    tooltip=[
                        alt.Tooltip('count()', title='Cantidad de Pasajeros'),
                        alt.Tooltip('Survived:N', title='Survived'),
                        alt.Tooltip('Pclass:N', title='Clases')]
                )
                .properties(title='Gráfico de Barras - Clases y Supervivencia',width=700,height=400)
                .configure_axis(grid=False)
                .configure_axisY(orient='right')
                .configure_legend(orient='left')
                .add_selection(interval)
                .transform_filter(interval)
            )
            st.altair_chart(chart_clase_supervivencia, use_container_width=True)

        # Gráfico de barras - Clases y Cantidad de Pasajeros
        with columna_derecha:
            interval = alt.selection_single(encodings=['color'])
            chart_clase_supervivencia_bar = (
                alt.Chart(df_filtered).mark_bar().encode(
                    alt.Y('Pclass:N', title='Clases'), 
                    alt.X('count():Q', title='Cantidad de pasajeros'),
                    color=alt.Color("Pclass:N", title="Clases", scale=alt.Scale(domain=[1, 2, 3], range=['#83B7E2','#25549C', '#647AD3'])),
                    tooltip=[
                        alt.Tooltip('count()', title='Cantidad de Pasajeros'),
                        alt.Tooltip('Pclass:N', title='Clases')]
                        )
                .properties(title='Gráfico de Barras - Clases y Cantidad de Pasajeros',width=700,height=400)
                .configure_axis(grid=False)
                .configure_legend(orient='right')
                .add_selection(interval)
                .transform_filter(interval)
            )
            st.altair_chart(chart_clase_supervivencia_bar, use_container_width=True)

st.write("##")
st.write("##")
with st.container():
    st.markdown("<h1 style='text-align: center;'>Supervivencia según Nivel de Cabina y Clase de Pasajero</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Este análisis interactivo revela patrones de supervivencia de pasajeros al explorar la distribución de supervivientes y fallecidos según el nivel de cabina. La información se segmenta por clases de pasajero, permitiendo una visión detallada de cómo estos factores se entrelazan. La tabla detallada y el gráfico de barras proporcionan una representación visual y cuantitativa de los datos, facilitando la comprensión de la influencia del nivel de cabina en la supervivencia en diferentes clases de pasajero, sin contar patrones nulos.</p>", unsafe_allow_html=True)

    # Filtro por Clase de Pasajero (Pclass)
    pclass_filter = st.selectbox('Filtrar por Clase de Pasajero (Pclass)', df['Pclass'].unique())

    # Preprocesamiento de datos con filtro
    df_con_cabina_filtrado = df[(df['Pclass'] == pclass_filter) & df['Cabin'].notna()].copy()
    df_con_cabina_filtrado['Cabin_Level'] = df_con_cabina_filtrado['Cabin'].str[0]

    # Contenedor de Resultados
    with st.container():
        # Estadísticas por nivel de cabina
        total_pasajeros = len(df_con_cabina_filtrado)
        estadisticas_por_cabina = df_con_cabina_filtrado.groupby('Cabin_Level')['Survived'].value_counts().unstack().fillna(0)

        # Crear tabla de resultados
        tabla_resultados = pd.DataFrame({
            "Cabinas": estadisticas_por_cabina.index,
            "Total de Pasajeros": estadisticas_por_cabina.sum(axis=1),
            "Supervivientes": estadisticas_por_cabina[1],
            "Fallecidos": estadisticas_por_cabina[0]
        })

        # Calcular porcentajes
        tabla_resultados["Porcentaje Supervivientes"] = (tabla_resultados["Supervivientes"] / tabla_resultados["Total de Pasajeros"]) * 100
        tabla_resultados["Porcentaje Fallecidos"] = (tabla_resultados["Fallecidos"] / tabla_resultados["Total de Pasajeros"]) * 100

        # Mostrar la tabla de resultados con formato
        st.table(tabla_resultados.set_index('Cabinas', drop=True).style 
        .set_properties(**{'text-align': 'center', 'font-size': '18px'})
        .bar(subset=['Total de Pasajeros', 'Supervivientes','Fallecidos', 'Porcentaje Supervivientes','Porcentaje Fallecidos'], color='#83B7E2')
        .highlight_max(axis=0, color='#ECF3FD')
        .format({'Total de Pasajeros': '{:.0f}', 'Supervivientes': '{:.0f}', 'Fallecidos': '{:.0f}','Porcentaje Supervivientes': '{:.0f}%', 'Porcentaje Fallecidos': '{:.0f}%'})
        .set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#ECF3FD'), ('color', '#000000'),
                                              ('font-size', '15px'), ('border', '1px solid #000000')]},
                {'selector': 'td', 'props': [('border', '1px solid #000000'), ('color', 'black')]},  # Añadido color negro
                {'selector': 'tr:hover', 'props': [('background-color', '#000000')]},
                {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#EDF3FD')]},
                {'selector': 'tr:nth-child(odd)', 'props': [('background-color', '#EDF3FD')]},
                {'selector': 'td:hover', 'props': [('background-color', '#3580E9'), ('color', 'White')]}
             ]))

        # Contenedor del Gráfico
        with st.container():
            interval = alt.selection_single(encodings=['color'])
            # Gráfico de barras de supervivencia por nivel de cabina
            chart_cabinas_supervivencia = (
                alt.Chart(df_con_cabina_filtrado).mark_bar().encode(
                    alt.X("count():Q", title="Cantidad de Pasajeros"),
                    alt.Y("Cabin_Level:N", title="Nivel de Cabina"),
                    color=alt.Color("Survived:N", title="Supervivencia", scale=alt.Scale(domain=[0, 1], range=['#83B7E2', '#25549C']))
                )
                .properties(width=1600, height=400, title='Gráfico de Barras - Cabinas y supervivencia')
                .configure_axis(grid=False)
                .add_selection(interval)
                .transform_filter(interval)
            )

            # Mostrar el gráfico de barras
            st.altair_chart(chart_cabinas_supervivencia, use_container_width=True)

st.write("##")
st.write("##")
# Iniciar contenedor de Streamlit
with st.container():
    # Títulos y presentación
    st.markdown("<h1 style='text-align: center;'> Explorando la Relación entre el Lugar de Embarque y Supervivencia</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>A través de visualizaciones intuitivas y estadísticas informativas, exploramos la relación entre el lugar de embarque de los pasajeros, su clase socioeconómica y su supervivencia durante el trágico evento. La aplicación ofrece una visión profunda de las distribuciones de pasajeros, destacando patrones y tendencias significativas que pueden arrojar luz sobre diversos aspectos de la tragedia del Titanic. Además, se presentan estadísticas detalladas y visualizaciones que permiten a los usuarios explorar y comprender mejor la complejidad de los datos relacionados con este histórico suceso.</p>", unsafe_allow_html=True)

    # Calcular estadísticas sobre supervivencia y fallecimiento por lugar de embarque
    total_pasajeros = len(df)
    total_por_clase = df.groupby('Embarked').size()
    supervivientes_por_clase = df[df['Survived'] == 1].groupby('Embarked').size()
    fallecidos_por_clase = df[df['Survived'] == 0].groupby('Embarked').size()

    # Crear un DataFrame con los resultados
    tabla_resultados = pd.DataFrame({
        "Categoria": ["Southampton", "Cherburgo", "Queenstown"],
        "Total de Pasajeros": total_por_clase.values,
        "Supervivientes": supervivientes_por_clase.values,
        "Fallecidos": fallecidos_por_clase.values
    })

    # Calcular porcentajes
    tabla_resultados["Porcentaje Supervivientes"] = (tabla_resultados["Supervivientes"] / tabla_resultados["Total de Pasajeros"]) * 100
    tabla_resultados["Porcentaje Fallecidos"] = (tabla_resultados["Fallecidos"] / tabla_resultados["Total de Pasajeros"]) * 100

    # Mostrar la tabla de resultados con formato
    st.table(tabla_resultados.set_index('Categoria', drop=True).style 
        .set_properties(**{'text-align': 'center', 'font-size': '18px'})
        .bar(subset=['Total de Pasajeros','Supervivientes','Fallecidos', 'Porcentaje Supervivientes','Porcentaje Fallecidos'], color='#83B7E2')
        .highlight_max(axis=0, color='#ECF3FD')
        .format({'Total de Pasajeros': '{:.0f}', 'Supervivientes': '{:.0f}', 'Fallecidos': '{:.0f}','Porcentaje Supervivientes': '{:.0f}%', 'Porcentaje Fallecidos': '{:.0f}%'})
        .set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#ECF3FD'), ('color', '#000000'),
                                              ('font-size', '15px'), ('border', '1px solid #000000')]},
                {'selector': 'td', 'props': [('border', '1px solid #000000'), ('color', 'black')]},  # Añadido color negro
                {'selector': 'tr:hover', 'props': [('background-color', '#000000')]},
                {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#EDF3FD')]},
                {'selector': 'tr:nth-child(odd)', 'props': [('background-color', '#EDF3FD')]},
                {'selector': 'td:hover', 'props': [('background-color', '#3580E9'), ('color', 'White')]}
             ]))

    with st.container():
        selected_class = st.multiselect("Seleccionar embarque", sorted(map(str, df['Embarked'].unique())))

        # Filtrar el DataFrame según las clases seleccionadas
        if selected_class:
            df_filtered = df[df['Embarked'].isin(selected_class)]
        else:
            df_filtered = df

        # Crear dos columnas para organizar los gráficos
        columna_derecha, columna_izquierda = st.columns((2, 2))

        # Gráfico de Barras - Lugar de Embarque y Cantidad de Pasajeros
        with columna_izquierda:
            interval = alt.selection_single(encodings=['color'])

            chart_embarked_supervivencia = (
                alt.Chart(df_filtered)
                .mark_bar()
                .encode(
                    y=alt.Y('Embarked:N', title='Embarque', axis=alt.Axis(labelAngle=0)),
                    x=alt.X('count():Q', title="Cantidad de Pasajeros", sort=alt.SortOrder('descending')),
                    color=alt.Color("Embarked:N", title="Lugar de Embarque", scale=alt.Scale(domain=['Q', 'S', 'C'], range=['#83B7E2', '#25549C', '#647AD3'])),
                    tooltip=[
                        alt.Tooltip('count()', title='Cantidad de Pasajeros'),
                        alt.Tooltip('Embarked:N', title='Lugar de Embarque')
                    ]
                )
                .properties(width=700,height=400,title='Gráfico de Barras - Embarques y Cantidad de Pasajeros')
                .configure_axis(grid=False)
                .configure_axisY(orient='right')
                .configure_legend(orient='left')
                .add_selection(interval)
                .transform_filter(interval)
            )
            st.altair_chart(chart_embarked_supervivencia, use_container_width=True)

        # Gráfico de Barras - Lugar de Embarque y Supervivencia
        with columna_derecha:
            interval = alt.selection_single(encodings=['color'])
            chart_clase_supervivencia = (
                alt.Chart(df_filtered).mark_bar().encode(
                    alt.X('Embarked:N', title='Clases', axis=alt.Axis(labelAngle=0)),
                    alt.Y('count():Q', title="Cantidad de Pasajeros"),
                    color=alt.Color("Survived:N", title="Supervivencia", scale=alt.Scale(domain=[0, 1], range=['#83B7E2', '#25549C'])),
                    tooltip=[
                        alt.Tooltip('count()', title='Cantidad de Pasajeros'),
                        alt.Tooltip('Survived:N', title='Supervivencia'),
                        alt.Tooltip('Embarked:N', title='Embarque'),
                    ]
                )
                .properties(width=700,height=400,title='Gráfico de Barras - Embarques y Supervivencia')
                .configure_legend(orient='right')
                .configure_axis(grid=False)
                .add_selection(interval)
                .transform_filter(interval)
            )
            st.altair_chart(chart_clase_supervivencia, use_container_width=True)

with st.container():
    st.markdown("<h1 style='text-align: center;'>Relación entre la Tarifa del Boleto y la Supervivencia en el Titanic</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Este análisis explora la relación entre el costo del boleto y la supervivencia de los pasajeros a bordo del Titanic. A través de estadísticas detalladas y visualizaciones interactivas, se examinan patrones y tendencias que pueden arrojar luz sobre la influencia del precio del boleto en el destino de los pasajeros durante el trágico evento del Titanic</p>", unsafe_allow_html=True)

    # Realizar cálculos y generar tabla de resultados
    total_pasajeros = len(df)
    total_sobrevivientes = df[df['Survived'] == 1].shape[0]
    total_muertos = df[df['Survived'] == 0].shape[0]

    # Calcular la tarifa total gastada por sobrevivientes y muertos
    tarifa_sobrevivientes = df.loc[df['Survived'] == 1, 'Fare'].sum()
    tarifa_muertos = df.loc[df['Survived'] == 0, 'Fare'].sum()

    tarifa_promedio_sobrevivientes = df[df['Survived'] == 1]['Fare'].mean()
    tarifa_promedio_muertos = df[df['Survived'] == 0]['Fare'].mean()

    tarifa_max_sobrevivientes = df[df['Survived'] == 1]['Fare'].max()
    tarifa_max_muertos = df[df['Survived'] == 0]['Fare'].max()

    tarifa_min_sobrevivientes = df[df['Survived'] == 1]['Fare'].min()
    tarifa_min_muertos = df[df['Survived'] == 0]['Fare'].min()

    # Combinar todas las columnas en la tabla de resultados
    tabla_resultados = pd.DataFrame({
        "Categoría": ["Sobrevivientes", "Fallecidos"],
        "Total Pasajeros": [total_sobrevivientes, total_muertos],
        "Tarifa Total": [tarifa_sobrevivientes, tarifa_muertos],
        "Tarifa Promedio": [tarifa_promedio_sobrevivientes, tarifa_promedio_muertos],
        "Tarifa Máxima": [tarifa_max_sobrevivientes, tarifa_max_muertos],
        "Tarifa Mínima": [tarifa_min_sobrevivientes, tarifa_min_muertos],
    })

    # Mostrar la tabla de resultados filtrada
    st.table(tabla_resultados.set_index('Categoría', drop=True).style 
        .set_properties(**{'text-align': 'center', 'font-size': '18px'})
        .bar(subset=['Total Pasajeros','Tarifa Total','Tarifa Promedio', 'Tarifa Máxima', 'Tarifa Mínima'], color='#83B7E2')
        .highlight_max(axis=0, color='#ECF3FD')
        .format({'Total Pasajeros': '{:.0f}', 'Tarifa Total': '{:.0f}$', 'Tarifa Promedio': '{:.0f}%', 'Tarifa Máxima': '{:.0f}$','Tarifa Mínima': '{:.0f}$'})
        .set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#ECF3FD'), ('color', '#000000'),
                                              ('font-size', '15px'), ('border', '1px solid #000000')]},
                {'selector': 'td', 'props': [('border', '1px solid #000000'), ('color', 'black')]},  # Añadido color negro
                {'selector': 'tr:hover', 'props': [('background-color', '#000000')]},
                {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#EDF3FD')]},
                {'selector': 'tr:nth-child(odd)', 'props': [('background-color', '#EDF3FD')]},
                {'selector': 'td:hover', 'props': [('background-color', '#3580E9'), ('color', 'White')]}
             ]))
    # Agregar un slider para filtrar por valores de Fare

    fare_slider = st.slider("Seleccionar rango de tarifas", float(df['Fare'].min()), float(df['Fare'].max()), (float(df['Fare'].min()), float(df['Fare'].max())))

    # Filtrar el DataFrame en función del rango seleccionado
    filtered_df = df[(df['Fare'] >= fare_slider[0]) & (df['Fare'] <= fare_slider[1])]

    interval = alt.selection_single(encodings=['color'])
    # Gráfico de dispersión con el DataFrame filtrado
    correlacion_chart = (
        alt.Chart(filtered_df).mark_circle(size=85).encode(
            x=alt.X('Fare', title='Precio del Boleto'),
            y=alt.Y('count()', title='Número de Pasajeros'),
            color=alt.Color("Survived:N", title="Sobrevivientes", scale=alt.Scale(domain=[0, 1], range=['#83B7E2', '#25549C'])),
            tooltip=[alt.Tooltip('count()', title='Cantidad de Pasajeros'), alt.Tooltip('Survived:N', title='Sobrevivientes'), alt.Tooltip('Fare', title='Precio del Boleto')]
        )
        .properties(width=1600, height=400)
        .add_selection(interval)
        .transform_filter(interval)
        .interactive()
    )

    # Mostrar el gráfico en Streamlit
    st.altair_chart(correlacion_chart, use_container_width=True)


st.write("---")
st.write("---")
with st.container():
    text_column,image_column = st.columns((3,2))
    with image_column:
        image = Image.open("Image/barco.png")
        st.image(image, width=500)
    with text_column:
        st.write("##")
        st.write("##")
        st.write("##")
        # Pie de página
        with st.container():
            st.markdown("<h1 style='text-align: center;'>Contactame</h1>", unsafe_allow_html=True)

            st.markdown("<h5 style='text-align: center;'>Email: <a href='mailto:AlvarezLucianoEzequiel@gmail.com'>AlvarezLucianoEzequiel@gmail.com</a></h5>", unsafe_allow_html=True)
            st.markdown("<h5 style='text-align: center;'>LinkedIn: <a href='https://www.linkedin.com/in/luciano-alvarez-332843285/'>Luciano Alvarez</a></h5>", unsafe_allow_html=True)
            st.markdown("<h5 style='text-align: center;'>GitHub: <a href='https://github.com/LUXI4NO'>Luciano Alvarez</a></h5>", unsafe_allow_html=True)


            st.markdown("""
                <p style='text-align: center;'>¡Gracias por visitar mi sitio! Espero poder ayudarte con tus datos.</p>
            """, unsafe_allow_html=True)
