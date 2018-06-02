import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

from ipywidgets import interact, fixed

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import plotly.figure_factory as ff
init_notebook_mode(connected=True)

def produtos_vendidos(vendas):
    
    produtos = list(vendas.DESCRICAO.value_counts()[:10].keys())
    
    trace1 = go.Bar(
        x=produtos,
        y=list(vendas[vendas.ANO == 2016].DESCRICAO.value_counts()[produtos].values),
        name='2016',
        text=list(vendas[vendas.ANO == 2016].DESCRICAO.value_counts()[produtos].values),
        textposition = 'auto',
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5),
            ),
        opacity=0.6
    )
    trace2 = go.Bar(
        x=produtos,
        y=list(vendas[vendas.ANO == 2017].DESCRICAO.value_counts()[produtos].values),
        text=list(vendas[vendas.ANO == 2017].DESCRICAO.value_counts()[produtos].values),
        textposition = 'auto',
        marker=dict(
            color='rgb(58,200,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5),
            ),
        opacity=0.6,
        name='2017'
    )
    
    trace3 = go.Bar(
        x=produtos,
        y=list(vendas[vendas.ANO == 2018].DESCRICAO.value_counts()[produtos].values),
        text=list(vendas[vendas.ANO == 2018].DESCRICAO.value_counts()[produtos].values),
        textposition = 'auto',
        marker=dict(
            color='rgb(79,112,247)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5),
            ),
        opacity=0.6,
        name='2018*'
    )

    data = [trace1, trace2, trace3]

    trace3 = dict(
        x=list(vendas.DESCRICAO.value_counts()[:10].keys()),
        y=list(vendas.DESCRICAO.value_counts()[:10].values),
        name='All'
    )

    updatemenus = list([
        dict(
            active=0,
            buttons=list([ 
                dict(
                    label = 'Ambos',
                     method = 'update',
                     args = [{'visible': [True, True, True]}]),
                dict(
                    label = '2016',
                     method = 'update',
                     args = [{'visible': [True, False, False]}]),
                dict(label = '2017',
                     method = 'update',
                     args = [{'visible': [False, True, False]}]),
                dict(label = '2018*',
                             method = 'update',
                             args = [{'visible': [False, False, True]}])
                          ]))
    ])

    layout = dict(title='Produtos vendidos', showlegend=True,
                  updatemenus=updatemenus)

    fig = go.Figure(data=data, layout=layout)
    iplot(fig)
    
def produto_por_unidade(vendas, produto, ano):
    
    traces = []
    lojas = np.unique(vendas.NOME.fillna('VERBO DIVINO'))
    for col in lojas:
        value = []
        for i in range(1, 13):
            value.append(vendas[vendas.DESCRICAO == produto][vendas.ANO == ano][vendas.NOME == col][vendas.MES == i].QUANTIDADE.sum())
        trace = go.Scatter(
                y=value,
                x=['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
                name=col,
                mode = 'lines+markers',
                opacity=0.6,
            )


        traces.append(trace)
        
        
        layout = dict(title='Produtos vendidos por loja', showlegend=True)
    
    fig = go.Figure(data=traces, layout=layout)
    iplot(fig)

def produto_por_tamanho(vendas, produto, ano, barras=True, pizza=True):
    
    traces = []
    pies = []
    tamanhos = ['00', '02', '04', '06', '08', 'PP', '12',  '14', 'PP', 'P', 'M', 'G', 'GG']
    lojas = np.unique(vendas.NOME.fillna('VERBO DIVINO'))
    posicoes = [
        {'x': [0, .5], 'y': [0, .46]},
        {'x': [.52, 1], 'y': [0, .46]},
        {'x': [0, .5], 'y': [.53, 1]},
        {'x': [.52, 1], 'y': [.53, 1]},
    ]
    annotations = []
    
    for i, col in enumerate(lojas):
        value = []
        for tam in tamanhos:
            value.append(vendas[vendas.DESCRICAO == produto][vendas.NOME == col][vendas.ANO == ano][vendas.TAMANHO == tam].QUANTIDADE.sum())
        
        trace = go.Bar(
                y=value,
                x=['N 00', 'N 02', 'N 04', 'N 06', 'N 08', 'N 10', 'N 12', 'N 14', 'PP', 'P', 'M', 'G', 'GG', 'ESP', 'ESPECIAL'],
                name=col,
                opacity=.75,
            )
                
        pie = go.Pie(
            labels = tamanhos,
            values = value,
            domain = posicoes[i],
            hoverinfo='value+percent', 
            textinfo='label',
            textfont=dict(size=12),
            marker=dict(line=dict(color='#ffffff', width=1)),
            opacity=.8
        )
        
        annotations.append({
            "font": {
                "size": 12
            },
            "showarrow": False,
            "text": col,
            "x": posicoes[i]["x"][0],
            "y": posicoes[i]["y"][1],
        })
                
        pies.append(pie) 

        traces.append(trace)       
        
    layout = dict(title='Produtos vendidos por tamanho - Quantidade', showlegend=True, barmode='stack')
    
    fig = go.Figure(data=traces, layout=layout)
    
    if barras:
        iplot(fig)
    
    fig2 = go.Figure(data=pies, layout= {'title': "Produtos vendidos por tamanho - Percentual", 'annotations':annotations})
    
    if pizza:
        iplot(fig2)

def dist_time(vendas):

    # Add histogram data
    x1 = sorted(vendas[vendas.ANO == 2016].HORA.fillna('09:00').apply(lambda h: float(h.replace(':', '.'))))
    x2 = sorted(vendas[vendas.ANO == 2017].HORA.fillna('09:00').apply(lambda h: float(h.replace(':', '.'))))
    x3 = sorted(vendas[vendas.ANO == 2018].HORA.fillna('09:00').apply(lambda h: float(h.replace(':', '.'))))

    # Group data together
    hist_data = [x1, x2, x3]

    group_labels = ['2016', '2017', '2018']

    # Create distplot with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels, bin_size=1)
    fig['layout'].update(title="Distribuição das vendas durante o dia.")

    # Plot!
    iplot(fig)